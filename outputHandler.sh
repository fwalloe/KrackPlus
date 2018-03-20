#!/bin/bash

input=$1
fileContent=""
newFileContent=""
diff=""
macIP=""
addedMac=""
addedIP=""
vulnMac=""
vulnIP=""
notVulnMac=""
notVulnIP=""
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

while true; do

newFileContent=$(cat $input 2> /dev/null)
diff=$(diff <(echo "$newFileContent") <(echo "$fileContent"))
fileContent="$newFileContent"

#Make newline the only separator in this subshell
IFS=$'\n'

#Unique elements only
macAndIP=$(printf "$diff" 2> /dev/null | grep "DHCP reply" 2> /dev/null | uniq)

# Adding mac and IP-address of connected clients
for line in $macAndIP; do
    addedMac="$(printf $line 2> /dev/null | cut -b 25- | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null | uniq)"
    addedIP="$(printf $line 2> /dev/null | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}' | uniq 2> /dev/null)"
    # Add mac and IP (if there is any)
    if [[ $(echo $addedMac | wc -c) -gt 5 && $(echo $addedIP | wc -c) -gt 5 ]]; then
        mac="$mac$addedMac\n"
        IP="$IP$addedIP\n"
        macIP="$macIP$addedMac $addedIP\n"
        printf "device with mac-address $addedMac connected\n\n"
    fi
done

#Discard recurring results
macIP="$(echo $macIP | uniq)"

#The mac-addresses vulnerable against pairwise key reinst.
pairwiseVuln=$(printf "$diff" 2> /dev/null | grep "Client is vulnerable to pairwise" 2> /dev/null | uniq)

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
       vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null))\n"
       echo "Found mac-address vulnerable to pairwise key reinstallation:"
       echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null
       printf "\n"
    done

    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(printf "$diff" 2> /dev/null | grep "Client is vulnerable to group" 2> /dev/null | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null)\n"
            echo "Found mac-address vulnerable to group key reinstallation:"
            printf $line 2> /dev/null | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null
            printf "\n"
    done
fi

#Discard duplicate results
vulnMac=$(printf $vulnMac 2> /dev/null | uniq)

notPairwiseVuln=$(printf "$diff" 2> /dev/null | grep "client DOESN'T seem vulnerable to pairwise" 2> /dev/null | uniq)

if [[ $(echo $notPairwiseVuln | wc -l) -gt 0 ]] ; then
    for line in $notPairwiseVuln; do
        notVulnMac="$notVulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null)\n"

        printf "Client $(printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null) does not seem vulnerable to pairwise 4-way handshake\n\n"
        done
    fi

notGroupVuln=$(printf "$diff" 2> /dev/null | grep "client DOESN'T seem vulnerable to group" 2> /dev/null | uniq)

if [[ $(echo $notGroupVuln | wc -l) -gt 0 ]] ; then
    for line in $notGroupVuln; do
        notVulnMac="$notVulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null)\n"

        printf "Client $(printf $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}' 2> /dev/null) does not seem vulnerable to group key handshake\n\n"
        done
fi

#Find the IP-addresses belonging to the mac-addresses
for line in $vulnMac ; do
   if [[ "$macIP" == *"$line"* ]] ; then
        vulnIP="$(printf $macIP 2> /dev/null | grep $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}')" 2> /dev/null
        printf "Vulnerable device:\nIP-address $vulnIP with mac-address $line\n\n"
        # Perform nmap scan if desired by the user
        if [[ $2 == "NMAP" ]]; then
            nmap="$vulnIP: $(nmapScan "$vulnIP" 2> /dev/null)\n"
            nmapOutput="$nmapOutput$nmap"
            printf "$nmap\n\n"
        fi
   fi
done

done
