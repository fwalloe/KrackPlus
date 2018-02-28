#!/bin/python

import optparse
import subprocess

def main():
    parse = optparse.OptionParser()
    
    #Adding option to run scan.                                                             TODO Task 2: Make scan of vulnerability work
    parse.add_option('--scan', '-s', default=False, help="This option will create a network with ssid 'testnetwork' where the default password is abcdefgh."
                     " Simply connect to the network and the scan will be executed against the connected device.")

    parse.add_option('--ssid', default='testnetwork', help="Use this option to set the SSID of the created network.")
    parse.add_option('--password', '-p', default='abcdefg', help="Use this option to set the password of the created network."
                     " Password length has to be 8 characters or more!")

    #Adding option to run attack against .....   
    parse.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....")

    options, args = parse.parse_args()

    # Running scan scripts
    if options.scan != False:
        print("Scanning " + options.scan + ":")
        subprocess.call(["./prepareClientScan.sh"])
        subprocess.call(["./findVulnerable/krackattack/krack-test-client.py"]) 
    
    # Running attack scripts
    elif options.attack != False:
        print("Performing key reinstallation attack against " + options.attack)
        #TODO subprocess, run attack script.
        
if __name__ == '__main__':
    main()


