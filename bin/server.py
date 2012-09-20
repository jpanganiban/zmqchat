#!/usr/bin/env python

import zmq


context = zmq.Context()


def responder(r_connection, b_connection):
    """Responds to received message and broadcasts
    it to all the connected clients."""
    responder = context.socket(zmq.REP)
    responder.bind(r_connection)
    broadcaster = context.socket(zmq.PUB)
    broadcaster.bind(b_connection)

    while True:
        # Receive request
        msg = responder.recv()
        # Broadcast message
        broadcaster.send(msg)
        # Response request
        responder.send(msg)

if __name__ == '__main__':
    port = raw_input("Enter your binding port: ")
    responder_connection = "tcp://0.0.0.0:%s" % (port)
    broadcaster_connection = "tcp://0.0.0.0:%s" % (int(port) + 1)
    print "Server now runs responder at %s and broadcaster at %s" % (port, int(port) + 1)
    responder(responder_connection, broadcaster_connection)
