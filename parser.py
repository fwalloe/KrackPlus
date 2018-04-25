#!/bin/python

###
#
# Issues: 
#	fails to save more than one ip/mac
#	should use something like findUnique so that only unique IPs/MACs are kept 
#	Save whether mac vulnerable to attack A and/or B in hashmap. 
#
###

import re	# used for regular expressions TODO: Har vi noen RE's?
import time
import subprocess

mac = ''
ip = ''
pairMacIP = {mac: ip}
groupVulnMacIP = {mac: ip}
pairwiseVulnMacIP = {mac: ip}

def scanParser():
	with open('./scanOutput.txt', 'r') as output:
		mac = ''
		ip = ''
		pairMacIP = {mac:ip}
                groupVulnMacIP = {mac:ip}
                pairwiseVulnMacIP = {mac:ip}
                counter = 0
                thePreviousDeviceTime = 0
		# goes through the file line by line
		while True:
		        time.sleep(0.5)
		        for line in output.readlines():
		                if (str("]")) in line:
		                        line = line.split(']')[1]
		                        # Filter out interesting lines and parse them
		                if (str("AP-STA-CONNECTED")) in line:
		                        connectedDevice = line.split("AP-STA-CONNECTED ")[1]
                                        # Taking time since last device connected, to end script after 60s
                                        #newDeviceTime = time()
                                        #if (newDeviceTime - thePreviousDeviceTime <= 60):
                                        #        thePreviousDeviceTime = newDeviceTime
                                        #        sys.exit()
		                        print "Device connected with MAC: " + connectedDevice
					print "Scanning " + connectedDevice
				if (str("DHCP reply")) in line:
		                        mac = (line.split('DHCP')[0])
					mac = (str(mac).strip())[:-1]
					ip = line.split('reply')[1]
					ip = (ip.split('to')[0]).strip()
					pairMacIP.update({mac:ip})
				if (str("vulnerable")) in line:
		                        if (str("DOESN'T")) in line:
		                                if (str("group")) in line:
							print (mac+" is not vulnerable to group key reinstallation")
						else:
							print (mac+" is not vulnerable to pairwise")  
					else:
						if str("group") in line:
							print (mac+" is vulnerable to group key reinstallation")
						else:
							print (mac+" is vulnerable to pairwise")
                                                        

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

		
def printDictionary(dictionary):
    # Prints everything in the dictionary.
    for key, value in dictionary.iteritems():
        if key != '' and value != '':
                print "Key: " + key + " has value: " + value

def writeDictionary(dictionary, file):
    with open(file, 'w') as MacIP:
        # Prints the dictionary to file
        for key, value in dictionary.iteritems():
            if key != '' and value != '':
                MacIP.write(key + '\n')
                MacIP.write(value + '\n')
    MacIP.closed

def writeResults():
    writeDictionary(pairMacIP, './scannedMacIP.txt')
    writeDictionary(pairwiseVulnMacIP, './pairwiseVulnMacIP.txt')
    writeDictionary(groupVulnMacIP, './groupVulnMacIP.txt')


