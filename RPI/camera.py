#!/usr/bin/python

import os

FILEPATH = "/home/pi/image.jpg"

def getCapture(filepath):
    os.system("raspistill -w 1024 -h 768 -e jpg -t 1 -o " + filepath)

if __name__ == '__main__':
    getCapture(FILEPATH)
