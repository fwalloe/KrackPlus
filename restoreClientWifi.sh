#!/bin/bash

#This script should (aggressively) restore wifi to wireles interfaces after either scan or attack. 

#TODO check if this helps
#service network-manager restart

sudo airmon-ng check kill >> /dev/null

sudo service NetworkManager restart
sudo service networking restart
nmcli radio wifi off
nmcli radio wifi on

# Restore intefaces by default names
if (ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':' | grep --quiet wlan0)
then
	ifconfig wlan0 down > /dev/null
	iwconfig wlan0 mode managed > /dev/null
	ifconfig wlan0 up > /dev/null
fi 

if (ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':' | grep --quiet wlan0mon)
then
 	ifconfig wlan0mon down > /dev/null
fi

#if (ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':' | grep --quiet wlan0sta1)
#then
# 	ifconfig wlan0sta1 down > /dev/null
#fi

#if (ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':' | grep --quiet wlan1sta1)
#then
# 	ifconfig wlan1sta1 down > /dev/null
#fi

#if (ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':' | grep --quiet wlan1)
#then
#	ifconfig wlan1 down > /dev/null
#	iwconfig wlan1 mode managed > /dev/null
#	ifconfig wlan1 up > /dev/null
#fi 

# Loop over and try to restore interfaces by name
#for i in {1..3}
#do
#	wlanName=$(ifconfig -a | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':')

#	if ! echo $wlanName | grep -q 'w';
#	then
#		ifconfig $wlanName down > /dev/null
#		iwconfig $wlanName mode managed > /dev/null
#		ifconfig $wlanName up > /dev/null
#	fi
#done

