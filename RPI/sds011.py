#!/usr/bin/python
# coding:utf8

import serial
import binascii

DATALEN = 10

def checkHeader(data):
    if data != 'aa':
        print("[ERROR] header check failed")
        exit(2)

def checkSum(data, sumHex):
    dataSum = 0
    for i in range(len(data)):
        dataSum += data[i]
    dataSumHex = hex(dataSum)
    if dataSumHex[-2:] != sumHex[-2:]:
        print("[ERROR] sum check failed")
        exit(3)

def getAqi():
    try:
        ser = serial.Serial(port = '/dev/ttyUSB0',
                            baudrate = 9600,
                            bytesize = serial.EIGHTBITS,
                            parity = serial.PARITY_NONE,
                            stopbits = serial.STOPBITS_ONE)
    except Exception, err:
        print("[ERROR] open serial failed")
        exit(1)

    dataHex = []
    dataDec = []
    buf = ser.read(DATALEN)
    for i in range(DATALEN):
        # turn into hex from binary (b2a_hex)
        hex = binascii.hexlify(buf[i])
        dataHex.append(hex)
        # turn into decimal from hex
        dataDec.append(int(hex, 16))
    checkHeader(dataHex[0])
    checkSum(dataDec[2:8], dataHex[8])
    pm25 = (dataDec[3] * 256 + dataDec[2]) / 10
    pm10 = (dataDec[5] * 256 + dataDec[4]) / 10
    return (pm25, pm10)

def main():
    aqi = getAqi()
    print("PM2.5: " + str(aqi[0]))
    print("PM10: " + str(aqi[1]))

if __name__ == '__main__':
    main()
