#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from gevent_zeromq import zmq
import select
import sys
import gevent
import json


context = zmq.Context()


def input(msg):
    select.select([sys.stdin], [], [])
    return sys.stdin.readline()


def subscriber(connection):
    socket = context.socket(zmq.SUB)
    socket.connect(connection)
    socket.setsockopt(zmq.SUBSCRIBE, '')
    while True:
        data = json.loads(socket.recv())
        print "%s: %s" % (data['alias'], data['message'])
        gevent.sleep(0)


def sender(connection, alias):
    socket = context.socket(zmq.REQ)
    socket.connect(connection)
    while True:
        message = input("")
        socket.send(json.dumps({'alias': alias, 'message': message}))
        msg_in = socket.recv()
        gevent.sleep(0)


if __name__ == '__main__':
    port = raw_input("Enter chat server port: ")
    alias = raw_input("Enter your chat alias: ")
    sender_connection = "tcp://0.0.0.0:%s" % (port)
    subscriber_connection = "tcp://0.0.0.0:%s" % (int(port) + 1)
    sender = gevent.spawn(sender, sender_connection, alias)
    subscriber = gevent.spawn(subscriber, subscriber_connection)
    gevent.joinall([subscriber, sender])
