#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from gevent_zeromq import zmq
import uuid
import select
import sys
import gevent
import json


context = zmq.Context()


def bold(text):
    """Make text bold"""
    return u'\033[1m%s\033[0m' % text


def input(msg):
    """Non-blocking raw_input."""
    sys.stdout.write("%s" % msg)
    select.select([sys.stdin], [], [])
    return sys.stdin.readline()


def subscriber(connection, sender_id):
    """Receives messages and prints it."""
    socket = context.socket(zmq.SUB)
    socket.connect(connection)
    socket.setsockopt(zmq.SUBSCRIBE, '')  # Don't filter subscription
    while True:
        data = json.loads(socket.recv())
        # Only print if it's not yourself.
        if data['sender_id'] != sender_id:
            sys.stdout.write("%s: %s" % (bold(data['alias']), data['message']))
        gevent.sleep(0)


def sender(connection, alias, sender_id):
    """Takes user input and sends message to server."""
    socket = context.socket(zmq.REQ)
    socket.connect(connection)
    while True:
        message = input("")
        socket.send(json.dumps({
            'alias': alias,
            'message': message,
            'sender_id': sender_id,
        }))
        msg_in = socket.recv()
        gevent.sleep(0)


if __name__ == '__main__':
    port = raw_input("Enter chat server port: ")
    alias = raw_input("Enter your chat alias: ")
    sender_connection = "tcp://0.0.0.0:%s" % (port)
    subscriber_connection = "tcp://0.0.0.0:%s" % (int(port) + 1)
    # Generate a sender_id
    sender_id = uuid.uuid4().hex
    sender = gevent.spawn(sender, sender_connection, alias, sender_id)
    subscriber = gevent.spawn(subscriber, subscriber_connection, sender_id)
    gevent.joinall([subscriber, sender])
