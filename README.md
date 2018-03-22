# KRACK+ #

This projects provides user interface to run KRACK scans and attempts to automate key reinstallation attacks. 


## Contributors ##
Lars Trinborgholen
Lars Mæhlum
Fredrik Walløe


## Files ##
krackPlus.py: graphical user interface for KrackPluss

prepareClientScan.sh: installs prerequisites necessary to run set up a network that check whether devices that connect to it are vulnerable

prepareClientAttack.sh. handles prerequsites necessary to run the attack script. 

reportTemplate.tex: a LaTeX template used to generate reports after vulnerability scans. Scan results are pushed to this file, which is compiled into a .pdf. 

restoreClientWifi.sh: attempts to restore client WIFI after an attack or scan

parser.py: parses output from either scan or attack and displays appropriate output to user.

networkCredentials.txt: file that hold credentials for the vulnerability scan network.


