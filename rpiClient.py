#!/usr/bin/python

import socket

HOST = "127.0.0.1"
PORT = 2016
ADDR = (HOST, PORT)
BUFSZ = 1024

if __name__ == '__main__':

    tcpSk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSk.connect(ADDR)
    print("connect to ECS Server successfully!")

    # make sure server is ECS
    tcpSk.send("I'm RPI")
    buf = tcpSk.recv(BUFSZ)
    if buf != "I'm ECS":
        print("the server is not ECS")
        tcpSk.close()
        exit()

    while True:
        buf = tcpSk.recv(BUFSZ)
        print("from ECS: " + buf)

    tcpSk.close()
