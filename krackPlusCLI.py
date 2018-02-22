#!/bin/python

import optparse
import subprocess

def main():
    parser = optparse.OptionParser()

    #Option to run KRACK vulnerability scan. 
    parser.add_option('--scan','-s', help="This option will create a network with SSID 'testnetwork' where the default password is 'abcdefgh'."
                     " Simply connect to the network and the scan will be executed against the connected device.", dest='scan', default=False, action='store_true')

    #Option to set the SSID for the created test network.
    parser.add_option('--ssid', default='testnetwork', help="Use this option to set the SSID for the created network.")

    #Option to set password for the created test network.
    parser.add_option('--password', '-p', default='abcdefgh', help="Use this option to set the password for the created network."
                     " Password length has to be 8 characters or more!")

    #Adding option to run attack against .....   
    parser.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....")

    options, args = parser.parse_args()

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


