# RTK Setup for Child and Parent Drones

**Overview**

The following approach provides centimeter-level GNSS (GPS/GLONASS) accuracy using an NTRIP client. The same setup is used on each drone.
There are two components, the base (UNAVCO station in Isla Vista) and the rovers (child drone, parent drone).
The below setup has been tested on the Pi and functions correctly.

**Hardware Setup**

* RPi Pin 1 (3.3V PWR)
* RPi Pin 9 (GND)
* RPi Pins 8 (TX), 10 (RX) (GPIO 14/15 on Zero W | GPIO 15/16 on 3 B+)
* u-blox NEO-M8P-02 RTK GNSS Receiver
* 6-pin JST connectors

Ordering of JST pins: VCC, GND, RX, TX, SCL, SDA (ignore SCL/SDA)

The UART serial port is disabled by default. To enable, follow these instructions: https://www.raspberrypi.org/documentation/configuration/uart.md

**Software Setup**

* ntrip.py - Retrieves RTCM data over an internet connection. Sends from Pi to NEO-M8P module over UART.
* read_gnss_data.py - Reads GNSS data sent from NEO-M8P over UART.

The two Python scripts run simultaneously. The operation is described below:
1. Pi connects to the internet and retrieves RTCM data through NTRIP client (ntrip.py)
2. Pi sends RTCM data to M8P module over UART (ntrip.py)
3. M8P module detects RTCM data and uses it to compute position corrections
4. M8P sends back accurate (centimeter-level) position data in NMEA format to Pi over UART (read_gnss_data.py)

**Programming Waypoint Navigation**

The ultimate goal is to use the GNSS data (in NMEA format) to program waypoint navigation. A simple NMEA parser can be found online to convert NMEA data
to longitude/latitude/altitude, which can be supplied and used with N3's Onboard SDK or with PX4. @Josh, @Richard, this is up to you both.
