#!/bin/bash

# Install dependencies
echo "Setting up dependencies..."


# Set interface variables:
wlan0=$(echo | ifconfig | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':')
wlan1=$(echo | ifconfig | sed 's/[ \t].*//;/^$/d' | awk "FNR==4" | tr -d ':')

# Verify that users have sufficient number of wireless interfaces
if [[ $wlan0 = *"w"* && $wlan1 = *"w"* ]];
then
	echo "Found $wlan0 and $wlan1"
else
	echo "Error: insufficient wireless interfaces found. You need an external NIC in addition to your internal NIC."
	exit
fi

# Replace hard-coded interface value in dnsmasq.conf
sed -i 1s/.*/interface=$wlan0/ krackattacks-poc-zerokey/krackattack/dnsmasq.conf

# Replace hard-coded interface values in enable_internet_forwarding.sh
sed -i 5s/.*/INTERNET=$wlan0/ krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh 
sed -i 7s/.*/REPEATER=$wlan1/ krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh 

# Make modified hostapd instance. Only needs to be done once
if [[ ! -x "./krackattacks-poc-zerokey/hostapd/hostapd" ]] 
then 
	echo "Compiling hostapd"
	cd ./krackattacks-poc-zerokey/hostapd/
	cp defconfig .config
	make -j 2 1>/dev/null
	cd ../../
fi

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
if ! cat hwEncryptionDisabled | grep -q '1';
then 
	echo "About to disable hardware encryption for NIC; this only needs to be done once"
	./findVulnerable/krackattack/disable-hwcrypto.sh
else 
	echo ""
fi

#Disable network, but ensure the script can still use wifi
sudo airmon-ng check kill >> /dev/null
sudo rfkill unblock wifi

# TODO Let user choose whether to reboot computer
## NOTE not implemented#TODO RUN: systool -vm ath9k_htc
