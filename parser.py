#!/bin/python

###
#
# Issues: 
#	fails to save more than one ip/mac
#	should use something like findUnique so that only unique IPs/MACs are kept 
#	Save whether mac vulnerable to attack A and/or B in hashmap. 
#
###

import re	# used for regular expressions

# parses list to make it unique NOT CURRENTLY USED
"""
def findUnique( toParse ):
	result = []
	seen = set()
	for i in toParse:
		if i not in seen:
			result.append(str(i).strip(','))
			seen.add(i)
	return result
"""
# open the file to parse and read line by line
with open('./forLars2.txt', 'r') as output:
	i = 0
	mac = ''
	ip = ''
	pairMacIP = { i: {'mac': mac, 'ip': ip} }
	# goes through the file line by line
	for line in output.readlines():
		# Filter out interesting lines and parse them
		if (str("DHCP reply")) in line:
			line = line.split(']')[1]
			mac = (line.split('DHCP')[0])
			mac = mac[:-2]
			#mac = (findUnique(mac))
			ip = line.split('reply')[1]
			ip = ip.split('to')[0]
			pairMacIP.update(i = {'mac': mac, 'ip': ip }) # does not update properly. And i does not work as a variable here.  
			i = i+1
		elif str("vulnerable") in line:
			line = line.split(']')[1]
			if str("DOESN'T") in line:
				if str("group") in line:
					print (mac+" is not vulnerable to group key reinstallation")
				else:
					print (mac+" is not vulnerable to pairwise")  
			else:
				if str("group") in line:
					print (mac+" is vulnerable to group key reinstallation")
				else:
					print (mac+" is  vulnerable to pairwise")  
				
	
#print ("mac: "+mac+" and ip: "+ip)

# Prints everything in the hashmap (must be expanded if we make it a hashmap with four values
for x in pairMacIP:
    print (x) # Can be removed as this is only a count
    for y in pairMacIP[x]:
        print (y,':',pairMacIP[x][y])



