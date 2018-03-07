#!/bin/bash

#### NOTE: Only install dependencies if not already installed. See second answer here for how to do that: 
# https://stackoverflow.com/questions/1298066/check-if-a-package-is-installed-and-then-install-it-if-its-not

# Install dependencies
echo "Setting up dependencies..."

#Checks whether dependencies are already installed; if not, installs them.
## NOTE / TODO maybe need to use gksudo with GUI
while read packages; do
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $packages | grep "install ok installed")
	if [ "" == "$PKG_OK" ]; then
		Package "echo $packages not found. Setting up $packages."
		apt-get -y update && apt-get install -y libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils python-scapy python-pycryptodome > /dev/null

		sudo apt-get --force-yes --yes install $packages
	fi

# Gets the list of dependencies from a file
done <dependenciesClientScan

# Make modified hostapd instance. Only needs to be done once. 
if [[ ! -x "./findVulnerable/hostapd/" ]] 
then 
	echo "Compiling hostapd"
	cd ./findVulnerable/hostapd/
	cp defconfig .config 
	make -j 2 > /dev/null
	cd ../../
fi

#Disable network
nmcli radio wifi off

# Disable hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
## NOTE we should also make sure that this is reversed when the user is done... Perhaps make it an option
./findVulnerable/krackattack/disable-hwcrypto.sh

#Let user choose whether to reboot computer
## NOTE not implemented

#### NOTE: next sections not done

#RUN: systool -vm ath9k_htc

## To check: the nohwcript/.. param has been set.

#Look for key reinstallations in the 4-way handshake
./findVulnerable/krackattack/krack-test-client.py

#Look for key reinstallations in the group key handshake 
#      ./krack-test-client.py --group


# Default network name:testnetwork 
# Default password: abcdefgh

### NOTE.: let user change this; must modify hostapd.conf
# You will probably have to edit the line `interface=` to specify the correct Wi-Fi interface to use for the AP.

