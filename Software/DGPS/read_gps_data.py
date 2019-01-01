# read_gps_data.py: This file reads the output of the GPS at pin 16 (RX)

#!/usr/bin/env python
import time
import serial

# Setup serial connection with serial port (UART pins 15, 16)
ser = serial.Serial(
        port='/dev/serial0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# Read NMEA data from GPS
while 1:
        nmea_data = ser.readline()
        print nmea_data
