#!/bin/python

# This script sniffs on an interface, captures and prints packets

from scapy.all import *
import optparse

# Prints packets
def pkt_callback(pkt):
    pkt.show()

# Interface parameter is needed
parse = optparse.OptionParser()
parse.add_option('--iface', '-i', default=True, help="This option selects interface to sniff on")
options, args = parse.parse_args()

# Start sniffing. It will continuously sniff until process is aborted
print "Sniffs of interface " + options.iface + "..."
sniff(iface=options.iface, prn=pkt_callback, filter="ip", store=0)

