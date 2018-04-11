#!/usr/bin/env python

# This script prints text to the reportTemplate.tex file

import subprocess
import re


# Get the hashmaps with MAC- and IP-addresses
# of scanned and vulnerable addresses
# from the scan output parser
# The format of the text can be found in the Latex code in the raw report file

#from parser import pairMacIP, pairwiseVulnMacIP, groupVulnMacIP

# Test block
# Should bo commented when functional. Uncomment the import above.

ip = ' '
mac = ' '
pairMacIP = {mac:ip}
pairwiseVulnMacIP = {mac:ip}
groupVulnMacIP = {mac:ip}

def addData():
    ip = '192.168.1.1'
    mac = '2222.aaaa.1111.2222'
    pairMacIP.update({mac:ip})

    ip = '192.168.1.2'
    mac = '3333.aaaa.1111.2222'
    pairMacIP.update({mac:ip})
    pairwiseVulnMacIP.update({mac:ip})

    ip = '192.168.1.3'
    mac = '4444.aaaa.1111.2222'
    pairMacIP.update({mac:ip})
    groupVulnMacIP.update({mac:ip})

    ip = '192.168.1.4'
    mac = '5555.aaaa.1111.2222'
    pairMacIP.update({mac:ip})

    ip = '192.168.1.5'
    mac = '6666.aaaa.1111.2222'
    pairMacIP.update({mac:ip})

# End test block

# Write a newline
def newline():
    return '\\newline'

def getParserData():
    counter = 1

    with open('./scannedMacIP.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line
                else:
                    ip = line
                    pairMacIP.update({mac:ip})
                counter += 1
    MACIP.closed

    counter = 1

    with open('./pairwiseVulnMacIP.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line
                else:
                    ip = line
                    pairwiseVulnMacIP.update({mac:ip})
                counter += 1
    MACIP.closed

    counter = 1

    with open('./groupVulnMacIP.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line
                else:
                    ip = line
                    groupVulnMacIP.update({mac:ip})
                counter += 1
    MACIP.closed

# Writes a line of text on a given line
# "lineNumber" is the line number on which this text will be written
# "str" is the string to be written on this line
def writeValue(report, string):
    #subprocess.call("sed -i '" + str(lineNumber) + "s/.*/" + string + newline() + "/'" + " ./reportTemplate.tex", shell=True)
    report.write(string + newline() + '\n')


# Writes the individual scanned device and the corresponding data
# "startLine" is the first line of the device's data
# "str" is the mac-address of the device
# "count" is just a number used to index them in the report
def writeElement(report, mac, count):
    writeValue(report, 'Device nr. ' + str(count))
    writeValue(report, 'Mac: ' + mac)
    writeValue(report, 'IP: ' + pairMacIP.get(mac))
    writeValue(report, '')
    if pairwiseVulnMacIP.get(mac) is not None and groupVulnMacIP.get(mac) is not None:
        writeValue(report, 'Not vulnerable')
    elif pairwiseVulnMacIP.get(mac) is not None or groupVulnMacIP.get(mac) is not None:
        writeValue(report, 'Vulnerable to')
        if (pairwiseVulnMacIP.get(mac)) is not None:
            writeValue(report, 'Pairwise Key Reinstallation Attacks')
        if (groupVulnMacIP.get(mac)) is not None:
            writeValue(report, 'Group Key Reinstallation Attacks')

    writeValue(report, '')
    writeValue(report, '')


# Writes about all the scanned devices
# "startLine" is the line number to begin the writing
def writeDocument():
    with open('./reportTemplate.tex', 'w') as report:
        with open('./texCode.txt', 'r') as initTexcode:
            texCode = initTexcode.read()
            report.write(texCode)
        initTexcode.closed

        count = 1
        for mac in pairMacIP.iterkeys():
            if (mac != ' '):
                writeElement(report, mac, count)
                count += 1
        report.write('\end{document}')
    report.closed


#addData()
getParserData()
# Write the mac-addresses to file
writeDocument()
