#!/bin/python

import re	# used for regular expressions

# open the file to parse and read line by line
with open('./forLars2.txt', 'r') as output:
	for line in output.readlines():
		if (str("DHCP reply")) in line:
			mac = (line.split(']')[1]) 
			mac = (mac.split('DHCP')[0])
			mac = mac[:-2]
			ip = line.split('reply')[1]
			ip = ip.split('to')[0]
			#mac line= mac.join(mac)
			print ("MAC: "+ str(mac))
			print ("IP: "+ip)
		elif str("vulnerable") in line:
			line = line.split(']')[1]
			print (line)
