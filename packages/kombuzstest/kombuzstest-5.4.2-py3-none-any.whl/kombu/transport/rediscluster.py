"""Redis transport module for Kombu.

Features
========
* Type: Virtual
* Supports Direct: Yes
* Supports Topic: Yes
* Supports Fanout: Yes
* Supports Priority: Yes
* Supports TTL: No

Connection String
=================
Connection string has the following format:

.. code-block::

    redis://[USER:PASSWORD@]REDIS_ADDRESS[:PORT][/VIRTUALHOST]
    rediss://[USER:PASSWORD@]REDIS_ADDRESS[:PORT][/VIRTUALHOST]

To use sentinel for dynamic Redis discovery,
the connection string has following format:

.. code-block::

    sentinel://[USER:PASSWORD@]SENTINEL_ADDRESS[:PORT]

Transport Options
=================
* ``sep``
* ``ack_emulation``: (bool) If set to True transport will
  simulate Acknowledge of AMQP protocol.
* ``unacked_key``
* ``unacked_index_key``
* ``unacked_mutex_key``
* ``unacked_mutex_expire``
* ``visibility_timeout``
* ``unacked_restore_limit``
* ``fanout_prefix``
* ``fanout_patterns``
* ``global_keyprefix``: (str) The global key prefix to be prepended to all keys
  used by Kombu
* ``socket_timeout``
* ``socket_connect_timeout``
* ``socket_keepalive``
* ``socket_keepalive_options``
* ``queue_order_strategy``
* ``max_connections``
* ``health_check_interval``
* ``retry_on_timeout``
* ``priority_steps``
"""

from __future__ import annotations

import functools
import numbers
import socket
from bisect import bisect
from collections import namedtuple
from contextlib import contextmanager
from queue import Empty
from time import time

from rediscluster import ClusterConnectionPool
from vine import promise

from kombu.exceptions import InconsistencyError, VersionMismatch
from kombu.log import get_logger
from kombu.utils.compat import register_after_fork
from kombu.utils.encoding import bytes_to_str
from kombu.utils.eventio import ERR, READ, poll
from kombu.utils.functional import accepts_argument
from kombu.utils.json import dumps, loads
from kombu.utils.objects import cached_property
from kombu.utils.scheduling import cycle_by_name
from kombu.utils.url import _parse_url

from . import virtual
from .redis import (
    Channel as RedisChannel,
    MultiChannelPoller,
    MutexHeld,
    QoS as RedisQoS,
    Transport as RedisTransport,
)

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None

try:
    import rediscluster
except ImportError:  # pragma: no cover
    rediscluster = None


logger = get_logger('kombu.transport.redis')
crit, warning = logger.critical, logger.warning

DEFAULT_PORT = 6379
DEFAULT_DB = 0

DEFAULT_HEALTH_CHECK_INTERVAL = 25

PRIORITY_STEPS = [0, 3, 6, 9]

error_classes_t = namedtuple('error_classes_t', (
    'connection_errors', 'channel_errors',
))



class MutexHeld(Exception):
    """Raised when another party holds the lock."""


@contextmanager
def Mutex(client, name, expire):
    """Acquire redis lock in non blocking way.

    Raise MutexHeld if not successful.
    """
    lock = client.lock(name, timeout=expire)
    lock_acquired = False
    try:
        lock_acquired = lock.acquire(blocking=False)
        if lock_acquired:
            yield
        else:
            raise MutexHeld()
    finally:
        if lock_acquired:
            try:
                lock.release()
            except redis.exceptions.LockNotOwnedError:
                # when lock is expired
                pass


def _after_fork_cleanup_channel(channel):
    channel._after_fork()

class QoS(RedisQoS):
    """Redis Ack Emulation."""

    restore_at_shutdown = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vrestore_count = 0

    def restore_visible(self, start=0, num=10, interval=10):
        self._vrestore_count += 1
        if (self._vrestore_count - 1) % interval:
            return
        with self.channel.conn_or_acquire() as client:
            ceil = time() - self.visibility_timeout
            try:
                with Mutex(client, self.unacked_mutex_key,
                           self.unacked_mutex_expire):
                    visible = client.zrevrangebyscore(
                        self.unacked_index_key, ceil, 0,
                        start=num and start, num=num, withscores=True)
                    for tag, score in visible or []:
                        self.restore_by_tag(tag, client)
            except MutexHeld:
                pass


class ClusterPoller(MultiChannelPoller):
    """Async I/O poller for Redis transport."""

    def _register(self, channel, client, conn, type):
        if (channel, client, conn, type) in self._chan_to_sock:
            self._unregister(channel, client, conn, type)
        if conn._sock is None:   # not connected yet.
            conn.connect()
        sock = conn._sock
        self._fd_to_chan[sock.fileno()] = (channel, conn, type)
        self._chan_to_sock[(channel, client, conn, type)] = sock
        self.poller.register(sock, self.eventflags)

    def _unregister(self, channel, client, type):
        self.poller.unregister(self._chan_to_sock[(channel, client, conn, type)])

    def _register_BRPOP(self, channel):
        """Enable BRPOP mode for channel."""
        conns = self._get_conns_for_channel(channel)

        for conn in conns:
            ident = (channel, channel.client, conn, 'BRPOP')

            if (conn._sock is None or ident not in self._chan_to_sock):
                channel._in_poll = False
                self._register(*ident)

        if not channel._in_poll:  # send BRPOP
            channel._brpop_start()

    def _register_LISTEN(self, channel):
        """Enable LISTEN mode for channel."""
        conns = self._get_conns_for_channel(channel)

        for conn in conns:
            ident = (channel, channel.subclient, conn, 'LISTEN')
            if (conn._sock is None or ident not in self._chan_to_sock):
                channel._in_listen = False
                self._register(*ident)

        if not channel._in_listen:
            channel._subscribe()  # send SUBSCRIBE

    def _get_conns_for_channel(self, channel):
        if self._chan_to_sock:
            return [conn for _, _, conn, _ in self._chan_to_sock]

        return [
            channel.client.connection_pool.get_connection_by_key(key, 'NOOP')
            for key in channel.active_queues
        ]

    def on_poll_start(self):
        for channel in self._channels:
            if channel.active_queues:           # BRPOP mode?
                if channel.qos.can_consume():
                    self._register_BRPOP(channel)
            if channel.active_fanout_queues:    # LISTEN mode?
                self._register_LISTEN(channel)

    def on_readable(self, fileno):
        try:
            chan, conn, type = self._fd_to_chan[fileno]
        except KeyError:
            return

        if chan.qos.can_consume():
            chan.handlers[type](**{'conn': conn})

    def handle_event(self, fileno, event):
        if event & READ:
            return self.on_readable(fileno), self
        elif event & ERR:
            chan, conn, type = self._fd_to_chan[fileno]
            chan._poll_error(type)

    def get(self, callback, timeout=None):
        self._in_protected_read = True
        try:
            for channel in self._channels:
                if channel.active_queues:           # BRPOP mode?
                    if channel.qos.can_consume():
                        self._register_BRPOP(channel)
                if channel.active_fanout_queues:    # LISTEN mode?
                    self._register_LISTEN(channel)

            events = self.poller.poll(timeout)
            if events:
                for fileno, event in events:
                    ret = self.handle_event(fileno, event)
                    if ret:
                        return
            # - no new data, so try to restore messages.
            # - reset active redis commands.
            self.maybe_restore_messages()
            raise Empty()
        finally:
            self._in_protected_read = False
            while self.after_read:
                try:
                    fun = self.after_read.pop()
                except KeyError:
                    break
                else:
                    fun()

    @property
    def fds(self):
        return self._fd_to_chan


class Channel(RedisChannel):
    """Redis Channel."""

    QoS = QoS

    _client = None
    _subclient = None
    _closing = False
    supports_fanout = True
    keyprefix_queue = '_kombu.binding.%s'
    keyprefix_fanout = '/{db}.'
    sep = '\x06\x16'
    _in_poll = False
    _in_listen = False
    _fanout_queues = {}
    ack_emulation = True
    unacked_key = 'unacked'
    unacked_index_key = 'unacked_index'
    unacked_mutex_key = 'unacked_mutex'
    unacked_mutex_expire = 300  # 5 minutes
    unacked_restore_limit = None
    visibility_timeout = 3600   # 1 hour
    priority_steps = PRIORITY_STEPS
    socket_timeout = None
    socket_connect_timeout = None
    socket_keepalive = None
    socket_keepalive_options = None
    retry_on_timeout = None
    max_connections = 10
    health_check_interval = DEFAULT_HEALTH_CHECK_INTERVAL
    fanout_prefix = True
    fanout_patterns = True
    global_keyprefix = ''
    queue_order_strategy = 'round_robin'

    _async_pool = None
    _pool = None

    from_transport_options = (
        virtual.Channel.from_transport_options +
        ('sep',
         'ack_emulation',
         'unacked_key',
         'unacked_index_key',
         'unacked_mutex_key',
         'unacked_mutex_expire',
         'visibility_timeout',
         'unacked_restore_limit',
         'fanout_prefix',
         'fanout_patterns',
         'global_keyprefix',
         'socket_timeout',
         'socket_connect_timeout',
         'socket_keepalive',
         'socket_keepalive_options',
         'queue_order_strategy',
         'max_connections',
         'health_check_interval',
         'retry_on_timeout',
         'priority_steps')  # <-- do not add comma here!
    )

    connection_class = redis.Connection if redis else None
    connection_class_ssl = redis.SSLConnection if redis else None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.ack_emulation:  # disable visibility timeout
            self.QoS = virtual.QoS
        self._registered = False
        self._queue_cycle = cycle_by_name(self.queue_order_strategy)()
        self.Client = self._get_client()
        self.ResponseError = self._get_response_error()
        self.active_fanout_queues = set()
        self.auto_delete_queues = set()
        self._fanout_to_queue = {}
        self.handlers = {'BRPOP': self._brpop_read, 'LISTEN': self._receive}

        if self.fanout_prefix:
            if isinstance(self.fanout_prefix, str):
                self.keyprefix_fanout = self.fanout_prefix
        else:
            # previous versions did not set a fanout, so cannot enable
            # by default.
            self.keyprefix_fanout = ''

        # Evaluate connection.
        try:
            self.client.ping()
        except Exception:
            self._disconnect_pools()
            raise

        self.connection.cycle.add(self)  # add to channel poller.
        # and set to true after sucessfuly added channel to the poll.
        self._registered = True

        # copy errors, in case channel closed but threads still
        # are still waiting for data.
        self.connection_errors = self.connection.connection_errors

        if register_after_fork is not None:
            register_after_fork(self, _after_fork_cleanup_channel)

    def _subscribe(self):
        keys = [self._get_subscribe_topic(queue)
                for queue in self.active_fanout_queues]
        print(keys)
        if not keys:
            return
        c = self.subclient
        # if c.connection._sock is None:
        #     c.connection.connect()
        self._in_listen = True
        c.psubscribe(keys)

    def _brpop_start(self, timeout=1):
        queues = self._queue_cycle.consume(len(self.active_queues))
        if not queues:
            return
        keys = queues
        self._in_poll = True

        node_to_keys = {}
        pool = self.client.connection_pool

        for key in queues:
            node = self.client.connection_pool.get_node_by_slot(pool.nodes.keyslot(key))
            node_to_keys.setdefault(node['name'], []).append(key)

        for chan, client, conn, cmd in self.connection.cycle._chan_to_sock:
            expected = (self, self.client, 'BRPOP')
            keys = node_to_keys.get(conn.node['name'])

            if keys and (chan, client, cmd) == expected:
                for key in keys:
                    conn.send_command('BRPOP', key, timeout)


    def _brpop_read(self, **options):
        try:
            dest__item = None
            conn = options.pop('conn', None)
            if conn:
                try:
                    dest__item = self.client.parse_response(conn,
                                                            'BRPOP',
                                                            **options)
                except self.connection_errors:
                    # if there's a ConnectionError, disconnect so the next
                    # iteration will reconnect automatically.
                    conn.disconnect()
                    raise
            if dest__item:
                dest, item = dest__item
                dest = bytes_to_str(dest).rsplit(self.sep, 1)[0]
                self._queue_cycle.rotate(dest)
                self.connection._deliver(loads(bytes_to_str(item)), dest)
                return True
            else:
                raise Empty()
        finally:
            self._in_poll = None

    def _create_client(self, asynchronous=False):
        params = {}
        if asynchronous:
            params['connection_pool'] = self.async_pool
        else:
            params['connection_pool'] = self.pool
        return self.Client(**params)

    def _get_pool(self, asynchronous=False):
        params = self._connparams(asynchronous=asynchronous)
        # self.keyprefix_fanout = self.keyprefix_fanout.format(db=params['db'])
        return ClusterConnectionPool(**params)

    def _get_client(self):
        return rediscluster.RedisCluster

class Transport(RedisTransport):

    Channel = Channel

    driver_type = 'redis-cluster'
    driver_name = driver_type

    implements = virtual.Transport.implements.extend(
        asynchronous=True, exchange_type=frozenset(['direct'])
    )

    def __init__(self, *args, **kwargs):
        if rediscluster is None:
            raise ImportError('dependency missing: redis-py-cluster')

        super().__init__(*args, **kwargs)
        self.cycle = ClusterPoller()

    def driver_version(self):
        return rediscluster.__version__
