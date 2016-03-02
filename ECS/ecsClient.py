#!/usr/bin/python

import sys
import socket
import os

HOST = "127.0.0.1"
UDPPORT = 2017
UDPADDR = (HOST, UDPPORT)
BUFSZ = 1024

def main(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(command, UDPADDR)
    (data, srvAddr) = client.recvfrom(BUFSZ)
    print(data)
    client.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[ERROR] wrong usage")
        exit(1)
    main(sys.argv[1])
