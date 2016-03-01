#!/usr/bin/python

import socket
import dht11
import bh1750

HOST = "127.0.0.1"
PORT = 2016
ADDR = (HOST, PORT)
BUFSZ = 1024

def openTcpSocket(address):
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.connect(address)
    return tcpSocket


def validateServer(tcpSocket):
    # validate client for server
    tcpSocket.send("I'm RPI")
    buf = tcpSocket.recv(BUFSZ)
    if buf != "I'm ECS":
        tcpSocket.close()
        print("[ERROR] the server is not ECS")
        exit(1)

def waitCmdAndExecute(tcpSocket):
    while True:
        command = tcpSocket.recv(BUFSZ)
        if command == "temperature":
            temp = dht11.getTemperature()
            tcpSocket.send(str(temp))
        elif command == "humidity":
            hum = dht11.getHumidity()
            tcpSocket.send(str(hum))
        elif command == "aqi":
            tcpSocket.send("I'm aqi")
        elif command == "light":
            light = bh1750.getLight()
            tcpSocket.send(str(light))
        else:
            tcpSocket.send("[ERROR] undefined command: " + command)
    tcpSocket.close()

def main():
    tcpSk = openTcpSocket(ADDR)
    print("connect ECS Server " + ADDR[0] + ":" + str(ADDR[1]) + " successfully")
    validateServer(tcpSk)
    waitCmdAndExecute(tcpSk)

if __name__ == '__main__':
    main()
