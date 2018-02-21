#!/bin/python

import optparse
import subprocess

def main():
    parse = optparse.OptionParser();
    
    ## TODO er det mulig å gjøre en slik type scan? I sciptet vi kjørte måtte vi sette opp et nettverk som man så måtte logge seg på. 

    #Adding option to run scan
    parse.add_option('--scan', '-s', default=False, help="This option will run a vulnerability scan against the given IP")

    #Adding option to run attack against .....
    parse.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against the given IP")
    
    #Adding option to install dependencies and turn of hardware encryption on NIC....etc.
    parse.add_option('--prepare', '-p', default=False, help="This option will prepare for scans and attacks. Takes 'scan', 'attack' for paramters for now.")
    
    ## TODO savner en kommentar her. Hva skjer her? Er det slik at vi sjekker om man allerede har satt opp requirements? I så fall vil ikke dette lagres mellom ver kjøring av programmet, slik det er satt opp nå. 
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


