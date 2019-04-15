#Import Functions
import serial
import string
import time

class openMV(object)
    def __init__(self, ser):
        self.ser = ser
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0

    def update():
        line = self.ser.readline()
        words = string.split(line,",")
        if len(words) == 8 and words[0] == 'X' and words[2] == 'Y' and words[4] == 'Z' and words[6] == 'R':
            self.x = float(words[1])
            self.y = float(words[3])
            self.z = float(words[5])
            self.r = float(words[7])
        else:
            self.x = 0
            self.y = 0
            self.z = 0
            self.r = 0
