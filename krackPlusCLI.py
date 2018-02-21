import optparse
import subprocess

def main():
    parse = optparse.OptionParser();
    
    #Adding option to run scan
    parse.add_option('--scan', '-s', default=False, help="This option will run vulnerability scan against the given IP")

    #Adding option to run attack against .....
    parse.add_option('--attack', '-a', default=False, help="This option will run attack against the given IP")
    
    #Adding option to install dependencies and turn of hardware encryption on NIC....etc.
    parse.add_option('--prepare', '-p', defaul=False, help="This option will prepare for scans and attacks. Takes 'scan', 'attack' for paramters for now.")
    
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
            subprocess.call(["prepareClientAttack.sh"])
            isClientPreparedAttack = True
        else:
            print("Already prepared for" + options.prepare + ". Please continue..")
            
    # Running scan scripts
    if options.scan != False:
        if isClientPreparedScan:
            print("Scanning" + options.scan + ":")
            subprocess.call(["vulnerabilityScan.sh"]) #TODO usikker på filnavnet her, kodet i bitbucket av alle ting.
    
    # Running attack scripts
    elif options.attack != False:
        if isClientPreparedAttack:
            print("Performing key reinstallation attack against " + options.attack)
            subprocess.call(["
        
if __name__ == '__main__':
    main()


