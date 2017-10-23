#My name is Charles Mugwagwa. 
#This is an implimentation of a program that gets speed information 
#from the switches and the processes so that the information can be used 
#dictate End Systems(e.g Access points) running on 100MB instead of gigabit.

#For NETMIKO installation, see netmiko_infor_accessor.py

from poe_Ip_list import * #list of IP's to ssh into.
from timeout_class import * #timeout class
from netmiko import ConnectHandler
from sys_name_extractor import *
import datetime
#from netmiko_infor_accessor import *

################################################################################
#Problems
################################################################################
#produces two files: speedtest.txt and get_100Fdx
#10.29.1.11 no data output from the speedtest file
#BakerVillage - error reading SSH protocol banner. Check BakerVillage Ip addresses. No pwr/poe.??
################################################################################

#creating list with strings from 1-48 for possible ports
port_list = list(range(1,48))
indx = 0
while indx < len(port_list):
    port_list[indx] = str(port_list[indx])
    indx += 1

def process(file_name,ip_address):
    #output --> appends to the given file
    #processes the 'int_custom.txt' file to a desirable format    
    print("process started")
    int_custom_file = open('int_custom.txt','r')    
    output = open(file_name,'a')    
    
    sys_file = open('sys_names_speed_test.txt','r') #process 'sys_names.txt' to get A.P name    
    sysNamesList = sysNameFunc(sys_file)   
    item = "no name"
    if sysNamesList[0] != None:
        item = sysNamesList[0]
    output.write(item+ " with ip address: " + str(ip_address)+"\n")
        
    #processing relevant lines and writing to output
    for line in int_custom_file:
        split_line = line.split()
        if len(split_line) != 0:            
            if split_line[0] in port_list:
                out_line = ""
                for x in split_line:
                    out_line = out_line + x + "     "                
                out_line = out_line + "\n"
                output.write(out_line)                
    output.close()
    int_custom_file.close()

def speedtest():
    #returns file with format: <port number> <status> <speed e.g 100Fdx>
    #output --> file: str(datetime.datetime.now())+".txt"
    print(" ")
    print("Note: The names of the buildings are in the module: poe_Ip_list , in the same dir!")    
    buildingList = input("Please enter the name of the building: ") 
    #check if valid buildingList
        
    file_name = "speedtest_"+str(datetime.datetime.now())+".txt"
    #/home/charlyman/Dropbox/Work/sys_names.txt        
    for ip_address in buildingList:                       
        loginSuccess = True
        with timeout(5, False, ip_address):
            ssh = ConnectHandler(device_type='hp_procurve',ip=ip_address, username='xxxxxxx',password='xxxxxxxx')
            print("Successful login!")                    
        if loginSuccess:
            
            #determine how many ports to iterate over
            file1 = open('speed_test.txt','w')
            file2 = open('sys_names_speed_test.txt', 'w')#/home/charlyman/Dropbox/Work/sys_names.txt 
            int_brief = ssh.send_command("show interfaces brief")
            file1.write(int_brief)
            file1.close()
            readfile = open('speed_test.txt','r')
            greatest = 0                       
            for line in readfile:
                x = line.split()
                if len(x) != 0:
                    if x[0] in port_list:
                        if int(x[0]) > greatest:
                            greatest = int(x[0])   
                            
            #ssh. run command for all the ports of the switch and write to file the output               
            int_custom_file = open('int_custom.txt','w')
            for x in range(1,greatest+1):
                command ="show interfaces custom "+str(x)+" port:2 status:1 speed:1"                
                int_custom = ssh.send_command(command)
                sys_info = ssh.send_command("show system information")
                int_custom_file.write(int_custom)
                file2.write(sys_info)
            int_custom_file.close()
            file2.close()                        
        process(file_name, ip_address) #for every switch
        print("Done with a switch.")
    file1.close() 
    
    def get_100Fdx(file_name): #output --> file:'get_100Fdx+datetime.txt'
        file = open(file_name,'r')
        file_name = "get_100Fdx"+str(datetime.datetime.now())+".txt"
        output = open(file_name,'w')
        line = file.readline()
        while line != "":
            split_line = line.split()
            if split_line[0] in port_list and len(split_line)>=3:
                if split_line[2] == '100FDx':
                    output.write(line)                      
            else:
                output.write(line)
            line = file.readline()
        output.close()  
        
    get_100Fdx(file_name) #get_100Fdx function call made here
        
    print("The script was successful!")

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    speedtest()
    end_time = datetime.datetime.now()
    time_taken = end_time - start_time
    print "time taken: "+str(time_taken)
