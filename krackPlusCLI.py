#!/bin/python

import optparse
import subprocess

def main():
    parse = optparse.OptionParser();
    

    #Adding option to run scan.                                                             TODO Task 2: Make scan of vulnerability work
    parse.add_option('--scan', '-s', default=False, help="This option will run a vulnerability scan against the given IP")

    #Adding option to run attack against .....                                              TODO Senere, one thing at a time.
    parse.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against the given IP")
    
    #Adding option to install dependencies and turn of hardware encryption on NIC....etc.   TODO Task 1: Make dependencies script work, and make sure all is good after doing this option.
    parse.add_option('--prepare', '-p', default=False, help="This option will prepare for scans and attacks. Takes 'scan', 'attack' for paramters for now.")
    
    options, args = parse.parse_args()

    # These bools are to be set to true, if client is already prepared.                     TODO Make a script to check.
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
#                                                                                           TODO Create this script.
            subprocess.call(["prepareClientAttack.sh"])
            isClientPreparedAttack = True
        else:
            print("Already prepared for" + options.prepare + ". Please continue..")

    # Running scan scripts
    if options.scan != False:
        if isClientPreparedScan:
            print("Scanning" + options.scan + ":")
            subprocess.call(["vulnerabilityScan.sh"])  #                    TODO Wrong filename, but this script exists
    
    # Running attack scripts
    elif options.attack != False:
        if isClientPreparedAttack:
            print("Performing key reinstallation attack against " + options.attack)
            #TODO subprocess, run attack script.
        
if __name__ == '__main__':
    main()


