apt-get update
apt-get install libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils python-scapy python-pycryptodome
./krackattacks-scripts/krackattack/disable-hwcrypto.sh
nmcli radio wifi off
sudo rfkill unblock wifi
