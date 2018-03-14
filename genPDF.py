#!/usr/bin/env python

# This script prints text to the reportTemplate.tex file

import subprocess

# Get the hashmap with MAC- and IP-addresses
# from the scan output parser
from parser import pairMacIP

# Appends a string to a given line
def writeValues( lineNumber , str):
    subprocess.call('sed -i "' + lineNumber + 's/$/' + str + ' /newline' + '/" ./reportTemplate.tex')

# Write the mac-addresses to file
    for key in pairMacIP.iteritems():
        writeValues(37, key)