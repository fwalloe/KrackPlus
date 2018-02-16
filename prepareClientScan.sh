#!/bin/bash/

# Install dependencies
apt-get -y update && apt-get install -y libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils python-scapy python-pycryptodome

# Compile modified hostapd instance
## NOTE this only needs to be done once; make check to avoid doing it every time
cd /findVulnerable/hostapd/
cp defconfig .config
make -j 2

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
cd ../krackattack/
./disable-hwcrypto.sh

#Let user choose whether to reboot computer
## NOTE not implemented

#### NOTE: next sections not done

#RUN: systool -vm ath9k_htc
## To check: the nohwcript/.. param has been set.

#Look for key reinstallations in the 4-way handshake
./krack-test-client.py

#Look for key reinstallations in the group key handshake 
#      ./krack-test-client.py --group


# Default network name:testnetwork 
# Default password: abcdefgh

### NOTE.: let user change this; must modify hostapd.conf
# You will probably have to edit the line `interface=` to specify the correct Wi-Fi interface to use for the AP.

