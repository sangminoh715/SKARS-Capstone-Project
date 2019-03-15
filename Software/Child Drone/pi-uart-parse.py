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
    words = string.split(line,",")
    if len(words) == 8 && words[0] == 'x' && words[2] == 'y' && words[4] == 'z' && words[6] == 'R':
        x = int(words[1])
        y = int(words[3])
        z = int(words[5])
        r = int(words[7])

    else:
        print(words);

    print("Valid Output")
    print(x,y,z,r)
