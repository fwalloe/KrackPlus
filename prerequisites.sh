apt-get update
apt-get install libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev net-tools git sysfsutils python-scapy python-pycryptodome
./krackattacks-scripts/krackattack/disable-hwcrypto.sh
nmcli radio wifi off
sudo rfkill unblock wifi

# i /etc/wpa_supplicant må det sjekkes om det finnes en wpa_supplicant.conf fil, hvis denne ikke finnes så må den lages.
# i wpa_supplicant.conf så må det stå:
# ctrl_interface=/var/run/wpa_supplicant
#      network={
#         ssid="Brennbakkvegen194"
#          key_mgmt=FT-PSK
#         psk="Sonic2016"
#      }



