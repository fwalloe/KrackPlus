#!/bin/bash

#This script should restore wifi to a wireless interface that is in monitoring mode. 

wlanName=$(iw dev | awk '/Interface/ {print $2}')

ifconfig $wlanName down
iwconfig $wlanName mode managed
ifconfig $wlanName up
