#My name is Charles Mugwagwa.
#This is an implementation of a timeout class that is used in various 
#netmiko functions e.g lldp_netmiko and lldp_speedtest

import signal

class timeout:
    def __init__(self, seconds=1,error_message='Timeout',ipAddress = None):
        self.seconds = seconds
        self.error_message = error_message
        self.ipAddress = ipAddress
    def handler_timeout(self, signum, frame):  
        print("")
        print("###########################################################################")
        print("Potential Bad IP: ", self.ipAddress)
        print ('login timeout! It is probably a bad IP.Check if poe_Ip_list is up to date.')
        print("###########################################################################")
        print("")
        print("")
        raise Exception("handler_timeout")
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handler_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)