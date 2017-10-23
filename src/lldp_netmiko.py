#My name is Charles Mugwagwa. 
#This is an implimentation of a program that gets lldp  information 
#from the switches and the processes so that the information
#can be used for faster problem solving in the future.

#For installing NETMIKO, see netmiko_infor_accessor.

from poe_Ip_list import * #list of IP's to ssh into
from sys_name_extractor import *
from netmiko_infor_accessor import *
import datetime 

global outputList
outputList = []

def process(): #processing lldp output to requested format
    global outputList    
    fromFile = open('lldp_output.txt','r')
    sysNamesFile = open('sys_names.txt', 'r')  
    file_name = "lldp_"+str(datetime.datetime.now())+'.txt'
    toFile = open(file_name,'a')    
    toFile.write("Time stamp: "+str(datetime.datetime.now())+"\n") 
    
    sysNamesList = sysNameFunc(sysNamesFile)    
    
    totalLines = sum(1 for line in fromFile) #sum up the lines in the whole file. determine eof        
    numbers = ['0','1','2','3','4','5','6','7','8','9']   
    fromFile.seek(0)#file reader goes to line(1)
    sentence = "port |    "+"serial   |  "+"     mac     |"+"        A.P Name       |"+"     Switch Name          | \n"
    out = sentence.split()        
    outputList.append(out)       
    toFile.write(sentence)
    sentence = "***************************************************************************************\n"
    out = sentence.split()
    outputList.append(out)    
    toFile.write(sentence)    
    linecount = 0
    sysNameIndex = 0    
    
    while linecount != totalLines+1: #while not eof       
        sentence = ""
        line = fromFile.readline().strip().split()
        linecount +=1        
        if line !=[]: #non-blank            
            if line[0]=='LLDP':
                sysName = sysNamesList[sysNameIndex]
                sysNameIndex += 1              
            if line[0][0] in numbers:#relevant lines                
                if len(line)==4: #hp switches. two lines of infor for 1 device
                    #print("Processing hp A.P.")                                        
                    if len(line[0]) == 2:#double digit . diff in spacing for them to be linear
                        sentence = sentence+line[0]+"    "+line[2]+"     "
                    else: #single digit                       
                        sentence = sentence+line[0]+"     "+line[2]+"     "
                    if linecount == totalLines: #if eof
                        break #stop processing the file by exiting the while loop.                    
                    line = fromFile.readline().strip().split()#next line of infor for same device
                    linecount += 1                                     
                    for x in line[2:8]:
                        sentence = sentence+x                                         
                    sentence = sentence+"     "+line[-1]+"     "+ sysName + "\n"                   
                    toFile.write(sentence)                    
                else: #Aruba. 1 line of infor for each device                
                    #print("processing a Non-Hp (probably aruba A.P.)")
                    sentence = sentence+line[0]+"                    "
                    for x in line[2:8]:
                        sentence = sentence+x
                    sentence = sentence+"     "+line[-1]+"     " + sysName + "\n"                  
                    toFile.write(sentence)    
    toFile.close()
    fromFile.close() 


def lldp():
    print(" ")
    print("Note: The names of the buildings are in the module: poe_Ip_list , in the same dir!")
    
    buildingList = input("Please enter the name of the building: ") 
    netmiko_infor_accessor(buildingList,'lldp_output.txt',"show lldp info remote-device")
    netmiko_infor_accessor(buildingList,'sys_names.txt',"show system information")
    process()
    print("The script was successful!") 

if __name__ == '__main__':
    lldp()
