from __future__ import absolute_import, unicode_literals
import time
from kombu import Exchange, Queue, Consumer
from kombu.mixins import ConsumerMixin
from pprint import pprint



from t.integration import transport

from case import skip


@skip.unless_module('redis')
class test_redis(transport.TransportCase):
    transport = 'redis'
    prefix = 'redis'

    def after_connect(self, connection):
        client = connection.channel().client
        client.info()

    def test_cannot_connect_raises_connection_error(self):
        conn = self.get_connection(port=65534)
        with self.assertRaises(conn.connection_errors):
            conn.connect()


@skip.unless_module('redis')
class TestRedisCluster(transport.TransportCase):
    transport = 'redis'
    prefix = 'redis'
    connection_options = {
        'hostname': 'redis-cluster01.dev.box.net'
    }

    def after_connect(self, connection):
        client = connection.channel().client
        client.info()

    def test_cannot_connect_raises_connection_error(self):
        conn = self.get_connection(port=65534)
        with self.assertRaises(conn.connection_errors):
            conn.connect()

    def test_Consumer(self):
        print("EXCHANGE:", self.exchange)
        print("QUEUE:", self.queue)
        print("CONNECTION:", self.connection)

        print('YO CONN:', self.connection)
        print(self.connection.channel())
        print("CONNECTED:", self.connected)
        q = Queue('foo', Exchange('foo'))
        cons = self.connection.channel().Consumer(q)
        assert isinstance(cons, Consumer)
        assert cons.channel is self.channel

    def test_redis_cluster_raises_exception(self):
        conn = self.get_connection(port=6379, timeout=5)
        print(dir(conn))
