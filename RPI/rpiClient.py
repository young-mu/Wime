#!/usr/bin/python

import socket
import sds011
import dht11
import bh1750
import camera
from time import sleep

HOST = "127.0.0.1"
PORT = 2016
ADDR = (HOST, PORT)
BUFSZ = 1024
PIECE = 4096

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

def sendFile(tcpSocket, filename):
    f = open(filename, 'rb')
    while True:
        piece = f.read(PIECE)
        if not piece:
            break;
        tcpSocket.send(piece)
    f.close()
    # ensure read buffer empty for ECS server
    sleep(1)
    tcpSocket.send("EOF")

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
            (pm25, pm10) = sds011.getAqi()
            tcpSocket.send(str(pm25) + "," + str(pm10))
        elif command == "light":
            light = bh1750.getLight()
            tcpSocket.send(str(light))
        elif command == "camera":
            filepath = "/tmp/image.jpg"
            camera.getCapture(filepath)
            sendFile(tcpSocket, filepath)
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
