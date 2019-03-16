#Import Functions
import serial
import string
import time

#Initialize Serial Object
ser = serial.Serial('/dev/ttyS0',baudrate=115200,timeout=0.5)
while(1):
    #Parse Data
    line = ser.readline()
    words = string.split(line,",")
    if len(words) == 8 and words[0] == 'X' and words[2] == 'Y' and words[4] == 'Z' and words[6] == 'R':
        x = float(words[1])
        y = float(words[3])
        z = float(words[5])
        r = float(words[7])
        print(x,y,z,r)
