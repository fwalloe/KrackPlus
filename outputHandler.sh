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
scanOutput=$(nmap -O $1 | grep 'OS details' 2> /dev/null)
echo $scanOutput
}

echo "Report"
echo ""

while true; do

newFileContent=$(cat $input 2> /dev/null)
diff="$(diff <(echo "$newFileContent") <(echo "$fileContent"))"
#diff=$(printf "$newFileContent" 2> /dev/null | grep -v "$fileContent" 2> /dev/null)
fileContent="$newFileContent"

#Make newline the only separator in this subshell
IFS=$'\n'

#Unique elements only
macAndIP=$(printf "$diff" 2> /dev/null | grep "DHCP reply" 2> /dev/null | uniq)

for line in $macAndIP; do
    addMac="$(printf $line 2> /dev/null | cut -b 25- | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null | uniq)"
    addIP="$(printf $line 2> /dev/null | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}' | uniq 2> /dev/null)"
    if [[ $(echo $addMac | wc -c) -gt 5 && $(echo $addIP | wc -c) -gt 5 ]]; then
        mac="$mac$addMac\n"
        IP="$IP$addIP\n"
        macIP="$macIP$addMac $addIP\n"
    fi
done

#Discard recurring results
macIP="$(echo $macIP | uniq)"

#The mac-addresses vulnerable against pairwise key reinst.
pairwiseVuln=$(printf "$diff" 2> /dev/null | grep "Client is vulnerable to pairwise" 2> /dev/null | uniq)

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    #echo "Clients vulnerable to pairwise key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
       vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null))\n"
       echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null
    done

    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(printf "$diff" 2> /dev/null | grep "Client is vulnerable to group" 2> /dev/null | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    #echo "Clients vulnerable to group key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null)\n"
        printf $line 2> /dev/null | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null
    done
    else
    echo "No clients vulnerable to group key reinstallations in the 4-way handshake"
fi

#echo ""

#Discard duplicate results
vulnMac="$(printf $vulnMac 2> /dev/null | uniq)"

#Find the IP-addresses belonging to the mac-addresses
#echo "IP-address of vulnerable mac-addresses:"
for line in $vulnMac ; do
   if [[ "$macIP" == *"$line"* ]] ; then
        vulnIP="$(printf "$macIP" 2> /dev/null | grep -s $line | grep -s -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}')" 2> /dev/null
        printf "$macIP" 2> /dev/null | grep $line 2> /dev/null | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}' 2> /dev/null
        if [[ $2 == "NMAP" ]]; then
            nmapOutput="$nmapOutput$vulnIP: $(nmapScan "$vulnIP")\n"
            printf $nmapOutput 2> /dev/null
        fi
   fi
done

done