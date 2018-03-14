#!/usr/bin/env python
import sys
import optparse
import subprocess
import atexit
import logging
import thread
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter
from subprocess import check_output
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

########   Examples which gives dirrent colored output    #################
#log.debug("A quirky message only developers care about")             WHITE
#log.info("Curious users might want to know this")                    GREEN
#log.warn("Something is wrong and any user should be informed")       YELLOW
#log.error("Serious stuff, this is red for a reason")                 RED
#log.critical("OH NO everything is on fire")                          SUPER RED/ORANGE

def main():
    parser = optparse.OptionParser()

   #Option to run KRACK vulnerability scan. 
    parser.add_option('--scan','-s', help="This option will create a network with SSID 'testnetwork' where the default password is 'abcdefgh'."
                     " Simply connect to the network and the scan will be executed against the connected device.", dest='scan', default=False, action='store_true')

    #Option to add nmap OS/Device detection against clients being scanned.
    parser.add_option('--os-detection', '-o', help="This option will add nmap OS/Device detection against clients being scanned", dest='os', default=False, action='store_true')

    #Option to set the SSID for the created test network.
    parser.add_option('--set-ssid', default='testnetwork', help="Use this option to set the SSID for the created network.", dest='ssid')

    #Option kto set password for the created test network.
    parser.add_option('--set-password', default='abcdefgh', help="Use this option to set the password for the created network."
                      " Password length has to be 8 characters or more!", dest='password')
    
    #Adding option to run attack against .....   
    parser.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....", dest='attack', action='store_true')

    options, args = parser.parse_args()

    # Running scan scripts
    # TODO we have two ifs here. Inner one should not be necessary. 
    if options.scan:
        #Write the credentials to file, so that they can be used next time the progran runs.
        with open('networkCredentials.txt', 'w') as netCredentials:
            netCredentials.write(options.ssid + '\n' + options.password)
	# TODO what is this?
        #thread.start_new_thread(parse, "scanOutput.txt")
        try:
            #Runs if user has specified custom wlan credentials
	    if options.ssid and options.password:
                subprocess.check_call(['./prepareClientScan.sh', 'customCredentials'])
            else:
                subprocess.call(["./prepareClientScan.sh"])
            log.warning("Connect to " + options.ssid + " with " + options.password + " to scan devices")
            log.info("Waiting for devices to connect...")
            #Create a wireless network and scan devices that connect to to it
	    with open('scanOutput.txt', 'w') as scanOutput:
                subprocess.call(["./findVulnerable/krackattack/krack-test-client.py &"], stdout=scanOutput, shell=True)
                subprocess.call(["./outputHandler.sh scanOutput.txt"], shell=True)
            #subprocess.call(["./outputHandler.sh outputFromScan.txt nmap"]) if options.os else subprocess.call(["./outputHandler.sh scanOutput.txt"])
        except KeyboardInterrupt:
            log.info("Generating PDF with findings...")
            log.info("Cleaning up...")
            subprocess.call(["./restoreClientWifi.sh"])
	    sys.exit(0)
        # if --os-detection:
        if options.os:
            print "NMAP"
        
    # Running attack scripts
    elif options.attack:
        print("Performing key reinstallation attack")
        #Sets up dependencies before the attack script runs
        subprocess.call(["./prepareClientAttack.sh"])
        #TODO subprocess, run attack script; note that this static implementation is only for testing purposes and should be removed. 	
        #subprocess.call(["./krackattacks-poc-zerokey/krackattack/krack-all-zero-tk.py wlan1 wlan0 Brennbakkvegen194 --target 54:27:58:63:14:aa"])

    # Must specify an option    
    else:
        log.warn("No option was given, please see usage below and try again!")
        parser.print_help()

if __name__ == '__main__':
    main()

