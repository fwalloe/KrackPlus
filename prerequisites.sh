#!/bin/bash

#This script sets up the pre-requisites for a Fast Transition (FT) vulnerability scan

apt-get update
apt-get install libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils python-scapy python-pycryptodome
./krackattacks-scripts/krackattack/disable-hwcrypto.sh
nmcli radio wifi off
sudo rfkill unblock wifi

#Variables
ssid=Brennbakkvegen194
psk=Sonic2016

#Creates wpa_supplicant if it does not already exist
if [ ! cd /etc/wpa_supplicant/wpa_supplicant.conf ]; then
	touch wpa_supplicant.conf
	printf "ctrl_interface=/var/run/wpa_supplicant\nnetwork={\nssid="$ssid"\nkey_mgmt=FT-PSK\npsk="$psk"}" > wpa_supplicant.conf
fi

# i /etc/wpa_supplicant må det sjekkes om det finnes en wpa_supplicant.conf fil, hvis denne ikke finnes så må den lages.
# i wpa_supplicant.conf så må det stå:
# ctrl_interface=/var/run/wpa_supplicant
#      network={
#         ssid="Brennbakkvegen194"
#          key_mgmt=FT-PSK
#         psk="Sonic2016"
#      }



