#!/bin/bash

# Installs dependencies
echo "Setting up dependencies..."

# Checks whether dependencies are already installed; if not, installs them.
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
if [[ ! -x "./findVulnerable/hostapd/hostapd" ]] 
then 
	echo "Compiling hostapd"
	cd ./findVulnerable/hostapd/
	cp defconfig .config 
	make -j 2 1>/dev/null
	cd ../../
fi

# Disables network
nmcli radio wifi off

# Disables hardware encryption, as bugs on some Wi-Fi network interface cards could interfere with the script used to check whether a client is vulnerable
if ! cat hwEncryptionDisabled | grep -q '1';
then 
	./findVulnerable/krackattack/disable-hwcrypto.sh
fi

# Replace default password if user requests it
sed -i "88s/.*/ssid=$(sed '1q;d' ./networkCredentials.txt)/" ./findVulnerable/hostapd/hostapd.conf
sed -i "1146s/.*/wpa_passphrase=$(sed '2q;d' ./networkCredentials.txt)/" ./findVulnerable/hostapd/hostapd.conf

