#!/bin/bash

input=$1
fileContent=""
newFileContent=""
diff=""
macIP=""
addMac=""
addIP=""

reportName='reportTemplate.tex'
reportPath='./'

#Make newline the only separator in the loop
IFS=$'\n'

# $1 is the output-string and $2 is the line number
writePDF() {
sed -i "$2s/.*/$1/" $reportPath$reportName
}

# $1 is the new file content
checkOutput() {

#Make newline the only separator in this subshell
IFS=$'\n'

output="$1"

#Unique elements only
macAndIP=$(printf "$output" | grep "DHCP reply" | uniq)

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
pairwiseVuln=$(printf "$output" | grep "Client is vulnerable to pairwise" | uniq)

vulnMac=""

if [[ $(echo $pairwiseVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to pairwise key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $pairwiseVuln; do
         #mac="$mac$(printf $line | awk '{print $2}' | cut -b 8-24)\n"
       vulnMac="$vulnMac$(echo $line | grep -Eo '*([0-9a-f]{2}\:){5}[0-9a-f]{2}')\n"
    done
    printf "$vulnMac\n"
    #writePDF $vulnMmac 43

    else
        echo "No clients vulnerable to pairwise key reinstallations in the 4-way handshake"
fi

#The mac-addresses vulnerable against group key reinst.
groupVuln=$(printf "$output" | grep "Client is vulnerable to group" | uniq)
if [[ $(echo $groupVuln | wc -l) -gt 0 ]]; then
    echo "Clients vulnerable to group key reinstallations in the 4-way handshake:"
    #Extract the mac-addresses from the output
    for line in $groupVuln; do
        #mac="$mac$(printf $line | awk '{print $2}' | cut -b 8-24)\n"
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
        printf "$macIP" | grep $line | grep -Eo '*([0-9]{1,3}\.){3}[0-9]{1,3}'
   fi
done

}

echo "Report"
echo " "


newFileContent=$(cat $input)
diff=$(printf "$newFileContent" | grep -v "$fileContent")
fileContent="$newFileContent"
#checkOutput "$diff"

checkOutput "$newFileContent"