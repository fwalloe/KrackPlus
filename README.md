# KRACK+ #

KrackPlus seeks to handle dependencies and parse the output from two scripts made by Mathy Vanhoef, that lets users scan their devices (to determine whether they are vulnerable to key reinstallation attacks) and attack those devices.

Users can run a scan or an attack with a single command – all dependencies are handled in the background. 

## Contributors ##
Lars Magnus Trinborgholen
Lars Kristian Mæhlum
Fredrik Walløe

## Usage ###

Run KrackPlus.py to see a usage guide.

## Files ##
KrackPlus.py: graphical user interface for KrackPlus.

prepareKrackPlus.sh: installs dependencies needed to run KrackPlus.

prepareClientScan.sh: installs prerequisites necessary to run set up a network that check whether devices that connect to it are vulnerable.

prepareClientAttack.sh. handles prerequsites necessary to run the attack script. 

reportTemplate.tex: a LaTeX template used to generate reports after vulnerability scans. Scan results are pushed to this file, which is compiled into a .pdf. 

restoreClientWifi.sh: attempts to restore client WIFI after an attack or scan.

parser.py: parses output from either scan or attack and displays appropriate output to user.

networkCredentials.txt: file that hold credentials for the vulnerability scan network.

dependenciesClientScan: contains a list of dependencies. Used by the prepareClient* scripts.

killProcesses: kills processes that run in the background (dnsmasq and, optionally, sslstrip).

generatePDF.py: creates a PDF report that contains scan results.

displayInterfaces.sh: finds and displays the names of the user's NICs as part of the usage guide. 
