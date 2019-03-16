#Import Functions
import serial
import string
import time

#Initialize Serial Object
ser = serial.Serial('/dev/ttyS0',baudrate=115200,timeout=1)

while(1):
    #Parse Data
    line = ser.readline()
    print(line)
