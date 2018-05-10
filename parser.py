#!/bin/python

import re	# used for regular expressions 
import datetime, time
import subprocess
import click

# global variables
mac = ''
ip = ''
pairMacIP = {mac: ip}
groupVulnMacIP = {mac: ip}
pairwiseVulnMacIP = {mac: ip}

# parses the output of a scan to display only key information to user
def scanParser():
    with open('./scanOutput.txt', 'r') as output:
        mac = ''
        ip = ''
        pairMacIP = {mac:ip}
        groupVulnMacIP = {mac:ip}
        pairwiseVulnMacIP = {mac:ip}
        counter = 0
        time_since_last_connected_device = 0
        PERIOD_OF_TIME = 90 # 1.5min
        number_of_connected_devices = 0
        should_continue=True

        # goes through the file line by line
        while should_continue:
            time.sleep(0.5)
			# Go through the file line by line, filter out interesting lines and parse them
            for line in output.readlines():

                if (str("]")) in line:
                    line = line.split(']')[1]
                if (str("AP-STA-CONNECTED")) in line:
                    connectedDevice = line.split("AP-STA-CONNECTED ")[1]
                    time_since_last_connected_device = time.time()
                    number_of_connected_devices += 1 
                    print "Device connected with MAC: " + connectedDevice
                    print "Scanning " + connectedDevice

                if (str("DHCP reply")) in line:
                    mac = (line.split('DHCP')[0])
                    mac = (str(mac).strip())[:-1]
                    ip = line.split('reply')[1]
                    ip = (ip.split('to')[0]).strip()
                    pairMacIP.update({mac:ip})

                if (str("vulnerable")) in line:
                    mac = (line.split(': ')[0])
                    if (str("DOESN'T")) in line:
                        if (str("group")) in line:
		                    print (mac+" is not vulnerable to group key reinstallation")
                        else:  
			                print (mac+" is not vulnerable to pairwise")  
                    else:
                        if str("group") in line:
                            print (mac+" is vulnerable to group key reinstallation")
                            groupVulnMacIP.update({mac:ip})
                        else:
                            print (mac+" is vulnerable to pairwise")
                            pairwiseVulnMacIP.update({mac:ip})

                if time.time() > time_since_last_connected_device + PERIOD_OF_TIME and time_since_last_connected_device > 0:
                    should_continue = False
                    exit
               
# writeParser parses the same file as scanParser, but does not output anything to screen. Used to fill hashmaps to generate report of scan results.
def writeParser():
    with open('./scanOutput.txt', 'r') as output:
        for line in output.readlines():
            if (str("]")) in line:
                line = line.split(']')[1]
            if (str("DHCP reply")) in line:
                mac = (line.split('DHCP')[0])
                mac = (str(mac).strip())[:-1]
                ip = line.split('reply')[1]
                ip = (ip.split('to')[0]).strip()
                pairMacIP.update({mac:ip})
            if (str("vulnerable")) in line:
                mac = (line.split(': ')[0])
                if str("group") in line:
                    groupVulnMacIP.update({mac:ip})
                else:
                    pairwiseVulnMacIP.update({mac:ip})

# parses output during an attack 
def attackParser():
	with open('./attackOutput.txt', 'r') as output:
		while True:
			for line in output.readlines():
				
				# Displays lines that contain any of the following strings
				if (
				str("Note") in line
				or str("Established MitM") in line 
				or str("Target network") in line
				or str("Will create rogue AP") in line 
				or str("Setting MAC address") in line
				or str("Giving the rogue") in line
				or str("Injecting Null frame so AP thinks") in line 
				or str("injected Disassociation") in line
				or str("2nd unique EAPOL msg3") in line
				or str("Performing key reinstallation attack!") in line 
				or str("forwarding EAPOL msg3") in line
				or str("Deauth") in line
				or str("failed") in line
				or str("WARNING") in line
				or str("SUCCESS") in line
				or str("interceptig its traffic") in line
				or str("hostapd") in line ):
					print line

# NOT IN USE		
def printDictionary(dictionary):
    # Prints everything in the dictionary.
    for key, value in dictionary.iteritems():
        if key != '' and value != '':
                print "Key: " + key + " has value: " + value

# writes results of a scan to files, in order to generate report     
def writeDictionary(dictionary, file):
    with open(file, 'w') as MacIP:
        # Prints the dictionary to file
        for key, value in dictionary.iteritems():
            if key != '' and value != '':
                MacIP.write(key + '\n')
                MacIP.write(value + '\n')
    MacIP.closed

# Writes the results of the scan to files
## it calls the writeParser to ensure that the hashmaps contain the results 
## then it calls writeDictionary three times to write the three hashmaps to three separate files 
def writeResults():
    writeParser()
    writeDictionary(pairMacIP, './scannedMacIP.txt')
    writeDictionary(pairwiseVulnMacIP, './pairwiseVulnMacIP.txt')
    writeDictionary(groupVulnMacIP, './groupVulnMacIP.txt')


