#!/usr/bin/python

import socket
import os

SKFILE = "/tmp/python_udp_socket"

if __name__ == '__main__':
    if os.path.exists(SKFILE):
        print("connect to ECS server...")
        client  = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        client.connect(SKFILE)
        print("connected!")

        client.send("hello")
        client.close()

    else:
        print("udp socket file does not exist!")
