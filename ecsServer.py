#!/usr/bin/python

import socket
import os

HOST = "0.0.0.0"
PORT = 2016
ADDR = (HOST, PORT)
BUFSZ = 1024
SKFILE = "/tmp/python_udp_socket"

if __name__ == '__main__':

    # tcpSk: ECS Server <---> RPI Client
    tcpSk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSk.bind(ADDR);
    tcpSk.listen(1);
    print("open ECS-RPI tcp socket")

    # udpSk: ECS Server <---> ECS Client
    udpSk = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    if os.path.exists(SKFILE):
        os.remove(SKFILE)
    udpSk.bind("/tmp/python_udp_socket");
    print("open ECS-ECS udp socket")

    print("ECS Server starts listening RPI Client...")
    (rpiConn, rpiAddr) = tcpSk.accept()
    try:
        rpiConn.settimeout(5)
        print("connected by " + rpiAddr[0] + ":" + str(rpiAddr[1]))

        # make sure client is RPI
        buf = rpiConn.recv(BUFSZ)
        if buf != "I'm RPI":
            print("the client is not RPI")
            rpiConn.close()
            exit()
        rpiConn.send("I'm ECS")

        while True:
            command = udpSk.recv(BUFSZ)
            rpiConn.send(command)
        udpSk.close()

    except socket.timeout:
        print("timeout!!!")
    rpiConn.close()
