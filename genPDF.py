#!/usr/bin/env python

##
# genPDF.py creates a PDF-report that shows the results of KrackPlus Scan
##

import subprocess
import re
import datetime
import sys

now = datetime.datetime.now()
pdf_name = "./krackPlus-vulnerability-report_" + str(now.day) \
           + "-" + str(now.month) + "-" + str(now.year) + "-" + str(now.hour) \
           + "-" + str(now.minute) + "-" + str(now.second)

# Get the hashmaps with MAC- and IP-addresses
# of scanned and vulnerable addresses
# from the scan output parser
# The format of the text can be found in the Latex code in the raw report file

#from parser import pairMacIP, vulnToPairwise, vulnToGroup

# Test block
# Should bo commented when functional. Uncomment the import above.

path = "./reports/"

# script should always be called with an argument, but if not, a default value will be used. 
path = sys.argv[1] if len(sys.argv) > 1 else "./reports/"

ip = ' '
mac = ' '
pairMacIP = {mac:ip}
vulnToPairwise = {mac:ip}
vulnToGroup = {mac:ip}

def addData():
    ip = '192.168.1.1'
    mac = '2222.aaaa.1111.2222'
    pairMacIP.update({mac:ip})

    ip = '192.168.1.2'
    mac = '3333.aaaa.1111.2222'
    pairMacIP.update({mac:ip})
    vulnToPairwise.update({mac:ip})

    ip = '192.168.1.3'
    mac = '4444.aaaa.1111.2222'
    pairMacIP.update({mac:ip})
    vulnToGroup.update({mac:ip})

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

# Parses data from three files to get the MAc-addresses of all clients seen during the scan, and whether they are vulnerable 
def getParserData():
    counter = 1

    # looks for MAC-addresses
    with open('./allScanned.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line.rstrip()
                else:
                    ip = line.rstrip()
                    pairMacIP.update({mac:ip})
                counter += 1
    MACIP.closed

    counter = 1

    with open('./vulnToPairwise.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line.rstrip()
                else:
                    ip = line.rstrip()
                    vulnToPairwise.update({mac:ip})
                counter += 1
    MACIP.closed

    counter = 1

    with open('./vulnToGroup.txt', 'r') as MACIP:
        for line in MACIP:
            if (line != ' '):
                if (counter % 2 == 1):
                    mac = line.rstrip()
                else:
                    ip = line.rstrip()
                    vulnToGroup.update({mac:ip})
                counter += 1
    MACIP.closed

# Writes a line of text on a given line
# "lineNumber" is the line number on which this text will be written
# "str" is the string to be written on this line
def writeValue(report, string):
    #subprocess.call("sed -i '" + str(lineNumber) + "s/.*/" + string + newline() + "/'" + " ./reportTemplate.tex", shell=True)
    report.write(string)

# Get a n mm long space
def getSpaces(n):
    return '\\hspace{' + str(n) + 'mm}'


# Writes the individual scanned device and the corresponding data
# "startLine" is the first line of the device's data
# "str" is the mac-address of the device
# "count" is just a number used to index them in the report
def writeElement(report, mac, count):

    writeValue(report, mac + ':' + getSpaces(14))

    if vulnToPairwise.get(mac) is None and vulnToGroup.get(mac) is None:
        writeValue(report, 'x')
    else:
        writeValue(report, getSpaces(1))
    writeValue(report, getSpaces(29))

    if (vulnToPairwise.get(mac)) is not None:
        writeValue(report, 'x')
    else:
        writeValue(report, getSpaces(1))
    writeValue(report, getSpaces(29))

    if (vulnToGroup.get(mac)) is not None:
        writeValue(report, 'x')
    else:
        writeValue(report, getSpaces(1))
    writeValue(report, getSpaces(29))

    writeValue(report, newline() + '\n')


# Writes about all the scanned devices
# "startLine" is the line number to begin the writing
def writeDocument():
    with open(pdf_name + ".tex", "w+") as report:
        with open('./initTexCode.txt', 'r') as initTexcode:
            texCode = initTexcode.read()
            report.write(texCode)
        initTexcode.close()

        count = 1
        for mac in pairMacIP.iterkeys():
            if (mac != ' '):
                writeElement(report, mac, count)
                count += 1
        report.write('\nIf KrackPlus lists a patched device as vulnerable, this likely means that the device contains a bug that allows for replayed broadcast and multicast frames.')
        report.write("\nNote also that if a device is vulnerable to the all-zero pairwise key reinstallation that affects Android 6.0 and Linux with wpa\_supplicant 2.3-2.6, the scan may fail to accurately gauge whether the device is vulnerable to key reinstallation attacks against the Group Key Handshake. Run KrackPlus with the --group option to test only the Group Handshake.")
        report.write('\end{document}')
    report.close()


#addData()
getParserData()
# Write the mac-addresses to file
writeDocument()
subprocess.call(["mkdir -p " + path], shell=True)
subprocess.call(["pdflatex " + pdf_name + ".tex > /dev/null"], shell=True)
subprocess.call(["mv " + pdf_name + ".pdf " + path + pdf_name + ".pdf"], shell=True)
subprocess.call(["rm " + pdf_name + ".tex > /dev/null"], shell=True)
subprocess.call(["rm " + pdf_name + ".aux > /dev/null"], shell=True)
subprocess.call(["rm " + pdf_name + ".log > /dev/null"], shell=True)
