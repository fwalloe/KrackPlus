#!/bin/python

import optparse
import subprocess

def main():
    parse = optparse.OptionParser();
    
    ## TODO Don't think it's possible to run a scan like this; the scan we ran earlier required us to set up a network that targets had to connect to. Perhaps we can force nearby clients to connect, but don't think we can just specify an IP

    #Adding option to run scan
    parse.add_option('--scan', '-s', default=False, help="This option will run a vulnerability scan against the given IP")

    #Adding option to run attack against .....
    parse.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against the given IP")
    
    #Adding option to install dependencies and turn of hardware encryption on NIC....etc.
    parse.add_option('--prepare', '-p', default=False, help="This option will prepare for scans and attacks. Takes 'scan', 'attack' for paramters for now.")
    
    ## TODO add comment to explain what happens here. If the intention is to avoid running prepare scans several times, then this will not work: can save to file to make it persistent. 
    options, args = parse.parse_args()
    isClientPreparedScan = False
    isClientPreparedAttack = False
    
    #Running prepare scripts for scan
    if options.prepare == 'scan':
        if isClientPreparedScan == False:
            print("Preparing client for " + options.prepare + " ...")
            subprocess.call(["prepareClientScan.sh"])
            isClientPreparedScan = True
        else:
            print("Already prepared for" + options.prepare + ". Please continue..")
    
    #Running prepare scripts for attack 
    elif options.prepare == 'attack':
        if isClientPreparedAttack == False:
            print("Preparing client for " + options.prepare + " ...")
	    #TODO dette scriptet finnes ikke. Har det bare ikke blitt pushet, eller?
            subprocess.call(["prepareClientAttack.sh"])
            isClientPreparedAttack = True
        else:
            print("Already prepared for" + options.prepare + ". Please continue..")
            
    ## TODO hvilket scan script? Vi kan med fordel ha mer utdypende kommentarer
    # Running scan scripts
    if options.scan != False:
        if isClientPreparedScan:
            print("Scanning" + options.scan + ":")
            subprocess.call(["vulnerabilityScan.sh"]) #TODO usikker paa filnavnet her, kodet i bitbucket av alle ting.
    
    # Running attack scripts
    elif options.attack != False:
        if isClientPreparedAttack:
            print("Performing key reinstallation attack against " + options.attack)
            #TODO her var det en halvferdig linje. Kommentert ut. 
            #subprocess.call(["
        
if __name__ == '__main__':
    main()


