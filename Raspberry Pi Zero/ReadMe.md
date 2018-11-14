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
sudo raspi-config
