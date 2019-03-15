#Import Functions
import serial
import string
import time

#Initialize Serial Object
ser = serial.Serial('/dev/ttyS0',baudrate=9600,timeout=0.5)

while(1):
    ser.flushInput();
    #Parse Data
    line = self.ser.readline()
    print(line)
    time.sleep(100)
