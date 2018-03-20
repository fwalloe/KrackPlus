#!/bin/bash

#This script should restore wifi to a wireless interface that is in monitoring mode. 

systemctl start NetworkManager

nmcli radio wifi off
nmcli radio wifi on


#As 
for i in {1..3}
do
	wlanName=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':')

	if ! echo $wlanName | grep -q 'w';
	then
		ifconfig $wlanName down
		iwconfig $wlanName mode managed
		ifconfig $wlanName up
	fi
done

# TODO check whether the wlan interfaces are back up; if not, advice user to remove their external NIC and click a button to run this script again. 
