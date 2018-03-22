#!/usr/bin/env python

# This script prints text to the reportTemplate.tex file

import subprocess

# Get the hashmaps with MAC- and IP-addresses
# of scanned and vulnerable addresses
# from the scan output parser
# The format of the text can be found in the Latex code in the raw report file

#from parser import pairMacIP, pairwiseVulnMacIP, groupVulnMacIP

# Test block
# Should bo commented when functional. Uncomment the import above.

ip = '192.168.1.0'
mac = '1111:aaaa:dddd:2222'
pairMacIP = {mac:ip}
pairwiseVulnMacIP = {mac:ip}
groupVulnMacIP = {mac:ip}

def addData():
    ip = '192.168.1.1'
    mac = '2222.aaaa.1111.2222'
    pairMacIP.update({mac:ip})

    ip = '192.168.1.2'
    mac = '3333.aaaa.1111.2222'
    pairMacIP.update({mac: ip})
    pairwiseVulnMacIP.update({mac:ip})

    ip = '192.168.1.3'
    mac = '4444.aaaa.1111.2222'
    pairMacIP.update({mac: ip})
    groupVulnMacIP.update({mac:ip})

    ip = '192.168.1.4'
    mac = '5555.aaaa.1111.2222'
    pairMacIP.update({mac: ip})

    ip = '192.168.1.5'
    mac = '6666.aaaa.1111.2222'
    pairMacIP.update({mac: ip})


addData()

# End test block


# Write a newline
def newline():
    return " \newline".encode('string_escape')


# Writes a line of text on a given line
# "lineNumber" is the line number on which this text will be written
# "str" is the string to be written on this line
def writeValue( lineNumber , string):
    #subprocess.call('sed -i "' + str(lineNumber) + 's/$/' + string + newline() + '/" ./reportTemplate.tex')
    return lineNumber + 1


# Writes the individual scanned device and the corresponding data
# "startLine" is the first line of the device's data
# "str" is the mac-address of the device
# "count" is just a number used to index them in the report
def writeElement(startLine , mac, count):
    line = startLine
    line = writeValue(line, "Device nr. " + str(count))
    line = writeValue(line, "Mac: " + mac)
    line = writeValue(line, "IP: " + pairMacIP.get(mac))
    line = writeValue(line, "")
    if pairwiseVulnMacIP.get(mac) is not None and groupVulnMacIP.get(mac) is not None:
        line = writeValue(line, "Vulnerable to")
        if (pairwiseVulnMacIP.get(mac)) is not None:
            line = writeValue(line, "Pairwise Key Reinstallation Attacks")
        if (groupVulnMacIP.get(mac)) is not None:
            line = writeValue(line, "Group Key Reinstallation Attacks")
    else:
        line = writeValue(line, "Not vulnerable")

    line = writeValue(line, "")
    line = writeValue(line, "")

    return line


# Writes about all the scanned devices
# "startLine" is the line number to begin the writing
def writeDocument(startLine):
    count = 1
    for mac in pairMacIP.iteritems():
        if (mac != ' '):
            startLine = writeElement(startLine, mac, count)
            count += 1


# Write the mac-addresses to file
lineNr = 51
writeDocument(lineNr)
