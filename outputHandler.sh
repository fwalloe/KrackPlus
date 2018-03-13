#!/bin/bash

input=$1
fileContent=""
newFileContent=""
diff=""
macIP=""
addMac=""
addIP=""
vulnMac=""
vulnIP=""
nmapOutput=""

reportName='reportTemplate.tex'
reportPath='./'

#Make newline the only separator in the loop
IFS=$'\n'

# $1 is the output-string and $2 is the line number
writePDF() {
sed -i "$2s/.*/$1/" $reportPath$reportName
}

# Performs an nMap scan on a given IP-adress
nmapScan() {
scanOutput=$(nmap -O $1 | grep 'OS details')
echo $scanOutput
}

echo "Report"
echo ""

while true; do

newFileContent=$(cat $input)
diff=$(printf "$newFileContent" | grep -v "$fileContent")
fileContent="$newFileContent"

#Make newline the only separator in this subshell
IFS=$'\n'

#Unique elements only
macAndIP=$(printf "$diff" | grep "DHCP reply" | uniq)

for line in $macAndIP; do
    addMac="$(printf $line | cut -b 25- | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' | uniq)"
    addIP="$(printf $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}' | uniq)"
    if [[ $(echo $addMac | wc -c) -gt 5 && $(echo $addIP | wc -c) -gt 5 ]]; then
        mac="$mac$addMac\n"
        IP="$IP$addIP\n"
        macIP="$macIP$addMac $addIP\n"
    fi
done

#Discard recurring results
macIP="$(echo $macIP | uniq)"

#The mac-addresses vulnerable against pairwise key reinst.
pairwiseVuln=$(printf "$diff" | grep "Client is vulnerable to pairwise" | uniq)

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to pairwise key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
         #mac="$mac$(printf $line | awk '{print $2}' | cut -b 8-24)\n"
       vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')\n"
       echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}'
    done

    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(printf "$diff" | grep "Client is vulnerable to group" | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to group key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')\n"
        printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}'
    done
    else
    echo "No clients vulnerable to group key reinstallations in the 4-way handshake"
fi

echo ""

#Discard duplicate results
vulnMac="$(printf $vulnMac | uniq)"

#Find the IP-addresses belonging to the mac-addresses
echo "IP-address of vulnerable mac-addresses:"
for line in $vulnMac ; do
   if [[ "$macIP" == *"$line"* ]] ; then
        vulnIP="$(printf "$macIP" | grep $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}')"
        printf "$macIP" | grep $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}'
        if [[ $2 == "NMAP" ]]; then
            nmapOutput="$nmapOutput$vulnIP: $(nmapScan "$vulnIP")\n"
            printf $nmapOutput
        fi
   fi
done

done