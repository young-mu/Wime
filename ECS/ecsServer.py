#!/usr/bin/python

import socket
import os

HOST = "0.0.0.0"
TCPPORT = 2016
UDPPORT = 2017
TCPADDR = (HOST, TCPPORT)
UDPADDR = (HOST, UDPPORT)
BUFSZ = 1024
PIECE = 4096

def openTcpSocket(address, listenNum):
    # tcpSocket: ECS server <---> RPI client
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind(address)
    tcpSocket.listen(listenNum)
    return tcpSocket

def openUdpSocket(address):
    # udpSocket: ECS Server <---> ECS Client
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind(address)
    return udpSocket

def validateClient(clientConnection):
    buf = clientConnection.recv(BUFSZ)
    if buf != "I'm RPI":
        clientConnection.close()
        print("[ERROR] the client is not RPI")
        exit(1)
    # validate server for client
    clientConnection.send("I'm ECS")

def recvFile(tcpSocket, filepath):
    f = open(filepath, 'wb')
    while True:
        piece = tcpSocket.recv(PIECE)
        if not data:
            break;
        f.write(piece)
    f.close()

def waitCmdAndTransfer(rpiClient, ecsClient):
    while True:
        (command, ecsAddr) = ecsClient.recvfrom(BUFSZ)
        rpiClient.send(command)
        if command == "camera":
            filepath = "/tmp/image.jpg"
            recvFile(rpiClient, filepath)
            ecsClient.sendto(filepath, ecsAddr)
        else:
            data = rpiClient.recv(BUFSZ)
            ecsClient.sendto(data, ecsAddr)
    ecsClient.close()

def main():
    print("open ECS-RPI tcp socket")
    tcpSk = openTcpSocket(TCPADDR, 1)
    print("open ECS-ECS udp socket")
    udpSk = openUdpSocket(UDPADDR)
    print("ECS server starts listening RPI client...")
    (rpiConn, rpiAddr) = tcpSk.accept()
    try:
        rpiConn.settimeout(5)
        print("connected by " + rpiAddr[0] + ":" + str(rpiAddr[1]))
        validateClient(rpiConn)
        # ECS server acts as a mediator
        waitCmdAndTransfer(rpiConn, udpSk)
    except socket.timeout:
        print("[ERROR] connection timeout")
    rpiConn.close()

if __name__ == '__main__':
    main()
