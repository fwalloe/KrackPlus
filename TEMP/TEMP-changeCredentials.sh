#!/bin/bash

SSID=$(sed '1q;d' networkCredentials.txt)
password=$(sed '2q;d' networkCredentials.txt)

sed -i '88s/.*/ssid=$SSID/' ./findVulnerable/hostapd/hostapd.conf
sed -i '1146s/.*/wpa_passphrase=$password/' ./findVulnerable/hostapd/hostapd.conf
