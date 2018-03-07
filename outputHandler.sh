#!/bin/bash

input=$1
mac=""
IP=""
macIP=""
NMAP=$2

reportName='reportTemplate.tex'
reportPath='./'

# $1 is the output-string and $2 is the line number

writePDF() {
sed -i "$2s/.*/$1/" $reportPath$reportName
echo test
}

echo "Report"
echo " "

#Unique elements only
macAndIP=$(cat $input | grep "DHCP reply" | uniq)

#Make newline the only separator in the loop
IFS=$'\n'

for line in $macAndIP; do
    #addMac=$(echo $line | awk '{print $7}' | cut -b 1-17)
    addMac=$(echo $line | cut -b 25- | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')
    #addIP=$(echo $line | awk '{print $5}')
    addIP=$(echo $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}')
    mac="$mac$addMac\n"
    IP="$IP$addIP\n"
    macIP="$macIP$addMac $addIP\n"
done

printf "IP-adresses that has been scanned:\n$IP\n"

#Reuse the mac-parameter
mac=""

#The mac-addresses vulnerable against pairwise key reinst.
pairwiseVuln=$(cat $input | grep "Client is vulnerable to pairwise" | uniq)

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to pairwise key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
         #mac="$mac$(printf $line | awk '{print $2}' | cut -b 8-24)\n"
       mac="$mac$(printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')\n"
    done
    printf "$mac\n"
    writePDF $mac 43

    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(cat $input | grep "Client is vulnerable to group" | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to group key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        #mac="$mac$(printf $line | awk '{print $2}' | cut -b 8-24)\n"
        mac="$mac$(printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')\n"
        printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}'
    done
    else
    echo "No clients vulnerable to group key reinstallations in the 4-way handshake"
fi
echo ""

#Discard duplicate results
mac=$(printf $mac | uniq)

#Find the IP-addresses belonging to the mac-addresses

echo "IP-address of vulnerable mac-addresses:"

for line in $mac ; do
   if [[ "$macIP" == *"$line"* ]] ; then
        printf $macIP | grep $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}'
   fi
done