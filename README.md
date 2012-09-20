ZMQCHAT
=======

A simple chat demonstration with ZeroMQ.

ZeroMQ: http://www.zeromq.org/


##Requirements

* python
* libevent (and libevent-dev to compile gevent)
* zeromq


##Installation

    cd /path/to/zmqchat/bin
    python setup.py install


##Server

    cd /path/to/zmqchat/bin
    ./zmqchat-server.py
    Enter your binding port: <enter a port>
    Server now runs responder at <selected port> and broadcaster at <selected port + 1>


##Client

    cd /path/to/zmqchat/bin
    ./zmqchat-client.ph
    Enter your chat server port: <enter a port>
    Enter your chat alias: <enter your alias>
    # Now start chatting


##Todo

* Daemonize server
* Run a test server
