#My name is Charles Mugwagwa.
#This is an implementation of a general netmiko information accessor. Provided 
#with a list of IP's, filename, and command, this function would ssh into each
#IP and write the resulting output information into the file provided.

################################################################################
#installation
################################################################################
#default python version >> 2.7.12
#netmiko requires paramiko installation
#download paramiko - 1.15.2. extract and cd into the directory using the terminal.
#to install run the command: sudo easy_install ./ , from the README file.
#download netmiko - 0.5.1. extract
#run "python setup.py build & python setup.py install"/"python setup.py --help"
#python2 is required for this module to work. You may have problems with python3
################################################################################

################################################################################
#To do list
################################################################################
# get uptime from sys_info
# google API for writing into a google sheet.


from timeout_class import *
from netmiko import ConnectHandler

def netmiko_infor_accessor(ip_list, file_name,command):
    file = open(file_name,'w') #/home/charlyman/Dropbox/Work/sys_names.txt 
    
    for ip_address in ip_list:                       
        loginSuccess = True
        with timeout(5, False, ip_address):
            ssh = ConnectHandler(device_type='hp_procurve',ip=ip_address, username='xxxxxx',password='xxxxxx')
            print("Successful login!")                    
        if loginSuccess:
            information = ssh.send_command(command)            
            file.write(information)     
    file.close()