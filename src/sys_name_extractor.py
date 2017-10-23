#My name is Charles Mugwagwa.
#This is an Implementation of a function that processes the output file(sys_names) of accessing
#information using the the commmand: sys_info = ssh.send_command("show system information")
#and then: sys_names.write(sys_info). 
#This function was implemented to be used by other netmiko functions that need to
#know the name of the switch that was ssh into.e.g. lldp_netmiko and lldp_speedtest

def sysNameFunc(sysNamesFile):
    #This function processes the sys_names.txt file to produce a list of the sys names
    lineSum = sum(1 for line in sysNamesFile)    
    sysNamesFile.seek(0)
    lineNum = 0
    sysNamesList = []
    while lineNum != lineSum+1:
        #process the file looking for sysNames and appending them to the list.        
        line = sysNamesFile.readline().strip().split()
        lineNum += 1        
        found = False
        sysName = None #initialization. to avoid referencing before assignment in line 29.
        while not found:
            if line != []:
                if line[1] == 'Name':
                    sysName = line[3]                    
                    found = True        
            if not lineNum == lineSum+1:
                line = sysNamesFile.readline().strip().split()
                lineNum += 1
            else:
                break #get out of the inner most loop              
        if sysName not in sysNamesList:
            sysNamesList.append(sysName)    
    return sysNamesList