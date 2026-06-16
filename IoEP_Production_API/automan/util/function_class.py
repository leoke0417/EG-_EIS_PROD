import socket, sys 
from thread import *

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
     
print('Socket Created')
 
host = '172.16.2.100';
port = 80;
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print('Hostname could not be resolved. Exiting')
    sys.exit()

class Function_class(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        constructor
        '''
        pass

    def cut_parameter(self,all_parameter):    
        set_parameter = all_parameter.split(',')
        dict_patameter = {}
        for parameter in set_parameter:
            dict_patameter[(parameter.split(':'))[0]] = (parameter.split(':'))[1]
        #print dict_patameter
        return dict_patameter

    def hostname_get(self,parameter):
        dict_patameter = functions.cut_parameter(parameter)
        #print dict_patameter
        result = socket.gethostname()
        return result

    def ipaddress_get(self,parameter):
        import netifaces
        import netifaces as ni
        result = ni.ifaddresses('eth0')[AF_INET][0]['addr']
        print(result)
        return result
    
    def vcpu_check(self,parameter):
        dict_patameter = functions.cut_parameter(parameter)
        print (dict_patameter)
        result = "vcpu_check"
        return result
    
    def open_cmd(self,parameter):
        os.system("start /wait cmd /c start python.bat")

    def ping_check(self,parameter):
        import re
        import subprocess
        import os
        list=[]

        list=parameter.split(',')
        
        if list[1]=="windows" :
            hostname = list[0]   
            output = subprocess.Popen(["ping.exe",hostname],stdout = subprocess.PIPE).communicate()[0]
    
            print(output)
    
            if ('unreachable' in output):
                print (hostname, 'is down!')
                return False
            else:
                print (hostname, 'is up!')
                return True
            
        elif list[1]=="linux":
            hostname = list[0]
            response = os.system("ping -c 1 " + hostname)

            #and then check the response...
            if response == 0:
                print (hostname, 'is up!')
                return True
            else:
                print (hostname, 'is down!')
                return False
            
functions = Function_class()
#p="ip:10.10.1.0,name:aaa"
#functions.cut_parameter(p)
#functions.hostname_verify(p)
