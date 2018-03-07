#!/bin/bash

input=$1
mac=""
IP=""
macIP=""
NMAP=$2

echo "Report"
echo " "

#Unique elements only
macAndIP=$(cat $input | grep "DHCP reply" | uniq)

#Make newline the only separator in the loop
IFS=$'\n'

for line in $macAndIP; do
    addMac=$(echo $line | awk '{print $7}' | cut -b 1-17)
    addIP=$(echo $line | awk '{print $5}')
    mac="$mac$addMac\n"
    IP="$IP$addIP\n"
    macIP="$macIP$addMac $addIP\n"
done

printf "Mac-addresses:\n$mac"

printf "IP-adresses:\n$IP"

printf "MACIP: $macIP"

#Reuse the mac-parameter
mac=""

#The mac-addresses vulnerable against pairwise key reinst.
pairwiseVuln=$(cat $input | grep "Client is vulnerable to pairwise" | uniq)

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to pairwise key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
        mac="$mac$(printf $line | awk '{print $2}' | cut -b 1-24)\n"
    done
    echo $mac
    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(cat $input | grep "Client is vulnerable to group" | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to group key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        mac="$mac$(printf $line | awk '{print $2}' | cut -b 1-24)\n"
        printf $line | awk '{print $2}' | cut -b 1-24
    done

    else
    echo "No clients vulnerable to group key reinstallations in the 4-way handshake"

fi

#Discard duplicate results
mac=$(printf $mac | uniq)
echo "MAC: $mac"
IFS=$' \n'
printf "MACip: $macIP"
#Find the IP-addresses belonging to the mac-addresses
for line in $mac; do
echo "if $line == $macIP"
    if  [[ $(echo $macIP | grep "$line" -c) -gt 0 ]] ; then
        #nmap -O $(printf $macIP | grep $line | awk '{print $2}')
        #printf $macIP | grep -E "$line" # | awk '{print $2}'
       # printf $mac | awk '{ print $2 }'
        echo "TREFF"
    fi
done

#TODO: Kjøre n-map mot vulnerable clients
