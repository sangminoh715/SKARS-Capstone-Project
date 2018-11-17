# Setup Guide For Raspberry Pi Zero W
## Basic Installation
1. Download Raspbian Lite from [official website](https://www.raspberrypi.org/downloads/)
1. Extract and flash image with [Etcher](https://www.balena.io/etcher/)
1. Create Empty file titled **ssh** to enable ssh by default
1. Create WiFi config file in boot folder wpa_supplicant.conf

For Home:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_SSID"
    psk="YOUR_WIFI_PASSWORD"
    key_mgmt=WPA-PSK
    id_str="home"
}
```
For UCSB Network:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
        ssid="UCSB Secure"
        scan_ssid=1
        key_mgmt=IEEE8021X
        eap=PEAP
        phase2="auth=MSCHAPV2"
        identity="your university login name"
        password="your password"
        id_str="school"
}
```
1. Insert SD Card and boot Pi
1. ssh into pi@raspberrypi.local (password: raspberry)

## Update
```
sudo raspi-config
sudo apt-get -y update
sudo apt-get -y upgrade
```

## Programs
* [**GPIO Control:**](https://gpiozero.readthedocs.io/en/stable/index.html) sudo apt install python3-gpiozero
* Enable I2C/SPI using *sudo raspi-config*
* [**I2C:**](http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2) *sudo apt-get install -y python-smbus i2c-tools*
* [**SPI:**](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md)
* **Web Server Stuff:** *sudo apt-get install apache2 php5 libapache2-mod-php5*

