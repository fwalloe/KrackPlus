#!/bin/bash

#This script should (aggressively) restore wifi to wireles interfaces after either scan or attack. 

systemctl start NetworkManager

nmcli radio wifi off
nmcli radio wifi on

# Restore main interface by default name 
ifconfig wlan0 down > /dev/null
iwconfig wlan0 mode managed > /dev/null
ifconfig wlan0 up > /dev/null

# Restore the external interface by default name 
ifconfig wlan1 down > /dev/null
iwconfig wlan1 mode managed > /dev/null
ifconfig wlan1 up > /dev/null

# Loop over and try to restore interfaces by name
for i in {1..3}
do
	wlanName=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':')

	if ! echo $wlanName | grep -q 'w';
	then
		ifconfig $wlanName down > /dev/null
		iwconfig $wlanName mode managed > /dev/null
		ifconfig $wlanName up > /dev/null
	fi
done

# TODO check whether the wlan interfaces are back up; if not, advice user to remove their external NIC and click a button to run this script again. 
