# Setup Guide For Raspberry Pi
## Installing OS onto microSD card
Note that it is easiest to do the setup by connecting the Raspberry Pi to your home WiFi via an Ethernet cable. It is even easier to do when you can hook up your Raspberry Pi to a display, but I will assume that the setup is being done headless.
1. Download Raspbian Lite from [official website](https://www.raspberrypi.org/downloads/).
1. Extract and flash image onto the microSD card with [Etcher](https://www.balena.io/etcher/).
1. On the microSD card with the flashed image, create Empty file titled **ssh** to enable ssh (which is not enabled by default).
1. Insert the microSD card into the slot on the Raspberry Pi. Connect all necessary cables (Ethernet, HDMI, USB, etc.) before powering on the Raspberry Pi. 

## Configuring Raspberry Pi
1. Find the IP address of the Raspberry Pi on your home network. If you have a display hooked up to your Raspberry Pi, this should be trivial. If you are doing the setup headless, you can use [Advanced IP Scanner](https://www.advanced-ip-scanner.com/) to scan the devices connected to your home network and find the IP address of the Raspberry Pi.
1. SSH into the Raspberry Pi using an SSH client by typing ```ssh pi@[IP Address]``` into the terminal. The default password is ```raspberry```.
1. Type ```sudo raspi-config``` into the terminal to open the menu for configuring the Raspberry Pi. From here, 
    1. Change your password (if you would like to).
    1. Change the network options for connecting to WiFi. For now, just use your home WiFi's SSID and password. This will let your Raspberry Pi connect to the Internet without an Ethernet cable. This is mainly important because you must set the WiFi country before you are allowed to connect to the Internet via WiFi.
    1. Change the interfacing options. Specifically, enable SSH, SPI, and I2C.
1. Type ```sudo apt-get -y update``` and ```sudo apt-get -y upgrade``` into the terminal to make sure that you are using the most updated version of Raspbian.

## Other Necessary Setup
Install other programs that you will use. I would recommend installing the following:
* A text editor if you are not familiar with ```nano``` (which is installed by default).
* [Samba](https://www.samba.org/) so that your Raspberry Pi can be reachable via its hostname (by default ```raspberrypi``` - you can also change this when configuring your Raspberry Pi). That is, on a network like your home LAN, you should be able to connect to your Raspberry Pi by typing ```ssh pi@raspberrypi.local``` (or if you changed your hostname, ```ssh pi@[YOUR HOSTNAME].local```). To download, type ```sudo apt-get install -y samba samba-common``` into the terminal. However, this will not work on *UCSB Secure* and *eduroam* because of how UCSB's network administrators set up the netmasks. If you wish, a work-around for this would be to assign a static IP address to your Raspberry Pi.

To connect to UCSB's WiFi, modify the following files accordingly (remember that you will need root access to modify these files).

**/etc/wpa_supplicant/wpa_supplicant.conf**

This is the file that your Raspberry Pi will look at when trying to figure out what network to connect to. The following setup will allow you to connect to both your home WiFi and UCSB's WiFi depending on which is available at the time. I referenced the [*eduroam* settings page](https://setup.wireless.ucsb.edu/help/faq-eduroam-settings) to find this information. Also, to get this to work, you don't need to copy the certificate into your Raspberry Pi.

```ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=us

network={
    ssid="[YOUR HOME NETWORK SSID]"
    psk="[YOUR HOME NETWORK PASSWORD]"
    priority=2
    id_str="home"
}

network={
    ssid="eduroam"
    scan_ssid=1
    key_mgmt=WPA-EAP
    eap=PEAP
    phase1="peaplabel=0"
    phase2="auth=MSCHAPV2"
    identity="[UCSBNetID]@ucsb.edu"
    password="[YOUR PASSWORD]"
    priority=1
    id_str="school"
}
```

**/etc/network/interfaces**

This is the file that your Raspberry Pi will look at when figuring out what network interface to use. We need it because connecting to a network that uses WPA Enterprise is slightly more complicated than connecting to a simple WPA network.

```
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

After making these changes, reconfigure the interface by typing ```wpa_cli -i wlan0 reconfigure```. You can also reboot the Raspberry Pi if you want. You can check to see that you are connected to the Internet by pinging some known server or by entering the command ```ip addr show``` and seeing that you have an assigned IP address under ```wlan0```.

**Note:** Again, due to how the UCSB network administrators set up *eduroam*, you are not able to simply SSH into your Raspberry Pi by typing ```ssh pi@raspberrypi.local```. You need to find the IP address that your Raspberry Pi was assigned. The netmask setup also makes it so that you aren't able to rely on Advanced IP Scanner since your Raspberry Pi might be assigned to a different subnet. The best way to find your Raspberry Pi's IP address is to either:
1. Connect your Raspberry Pi to a display and boot it. One of the last lines that shows up (before the login prompt) will be your assigned IP address (that is, if the WiFi setup is correct). 
1. Statically set your Raspberry Pi's IP address. *If you decide to do this, beware that IP address conflicts may occur when DHCP assigns a conflicting IP address to another device that wants to connect to UCSB's WiFi*.

## Other Programs
Functionality | Command
------------- | -------
[**GPIO Control**](https://gpiozero.readthedocs.io/en/stable/index.html) | ```sudo apt install python3-gpiozero```
[**I2C**](http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2) | ```sudo apt-get install -y python-smbus i2c-tools```
[**SPI**](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md) | 
**Web Server Stuff** | ```sudo apt-get install apache2 php5 libapache2-mod-php5```