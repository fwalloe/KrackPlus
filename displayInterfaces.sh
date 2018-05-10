#!/bin/bash

# Display a message that demonstrates the advised usage of --nic-mon and --nic-rogue-ap based on which NICs the user has. 

# Set interface variables:
wlan0=$(echo | ifconfig | sed 's/[ \t].*//;/^$/d' | awk "FNR==3" | tr -d ':')
wlan1=$(echo | ifconfig | sed 's/[ \t].*//;/^$/d' | awk "FNR==4" | tr -d ':')

# Only display message to users if they 
if [[ $wlan0 = *"w"* && $wlan1 = *"w"* ]];
then
	echo "Detected 2 network interface cards: $wlan0 and $wlan1."
	echo "To run perform an attack, use: --nic-mon $wlan0 --nic-rogue-ap $wlan1"
	  
else
	echo "Remember to plug in a second network interface card if you want to perform key reinstallation attacks."
fi

