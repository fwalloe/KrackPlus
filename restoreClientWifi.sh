#!/bin/bash

#This script should restore wifi to a wireless interface that is in monitoring mode. 

wlanName=$(iw dev | awk '/Interface/ {print $2}')

systemctl start NetworkManager

ifconfig $wlanName down
iwconfig $wlanName mode managed
ifconfig $wlanName up

# TODO check whether the wlan interfaces are back up; if not, advice user to remove their external NIC and click a button to run this script again. 
