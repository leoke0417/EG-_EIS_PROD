#coding=utf-8
'''
Created on 2010/12/28

@author: panda.huang
'''
import automan.tool.error as error
from automan.tool.verify import Verify
from pathlib import Path
import os.path
import cv2 as CV2
import paramiko, sys
#pip3 install opencv-python
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini' , 'Eonone.conf'),encoding="utf-8")

class Tool(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def file_create(self,value_dict):
        file = os.path.join(os.getcwd(),'temp',value_dict['value'])
        print(file)
        fd = os.open(file,os.O_RDWR|os.O_CREAT)
        os.close(fd)
    
    def full_verify(self,value_dict):
        print(value_dict["key"]=='：kkk')
        
    def file_exist_verify(self,value_dict):
        my_file = Path(value_dict["file"])
        if my_file.is_file() == True:
            return
        else:
            raise error.notfind()
        
    def file_verify(self):
        my_file = Path("test.txt")
        if my_file.is_file() == True:
            return
        else:
            raise error.notfind()
    
    def dir_list(self):
        return 100
    
    def test_get(self):
        raise error.notfind()

    def testerror_get(self):
        raise error.notfind()
    
    def dir_set(self,value_dict):
        print("test")
        pass
    
    def dir_verify(self,value_dict):
        local_dict = dict(value_dict)
        #get value from system
        try:
            system_value = local_dict['key']
            local_dict['system_value'] = system_value
            Verify().verify(local_dict)
        except error.equalerror:
            raise error.equalerror()
        except error.notequalerror:
            raise error.notequalerror()
        except:
            raise error.nonamevalue()
    def picture_verify(self,value_dict):
        local_dict = dict(value_dict)
        pic1 = local_dict['path']
        pic2 = local_dict['source_path']
        lessthan = local_dict['lessthan']
        img1 = CV2.imread(pic1)
        img2 = CV2.imread(pic2)
        hash1 = self.dHash(img1)
        hash2 = self.dHash(img2)
        dhashvalue = self.cmpHash(hash1, hash2)
        print(float(dhashvalue) , float(lessthan)) 
        if (float(dhashvalue) > float(lessthan)) :
            return 1
        
    def dHash(self, image):
        img = CV2.resize(image, (9, 8), interpolation=CV2.INTER_CUBIC)
        gray = CV2.cvtColor(img, CV2.COLOR_BGR2GRAY)
        hash_str = ''
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    def cmpHash(self, hash1, hash2):
        n = 0
        if len(hash1) != len(hash2):
            return -1
        for i in range(len(hash1)):
            if hash1[i] != hash2[i]:
                n = n + 1
        return n
        
    def getsystem(self,test):
        return '100'
        
    def SSH_command_run(self, valueDict):
        ##  Execute command line via SSH.
        ##
        ##  Needed package:
        ##      paramiko
        ##      sys
        ##
        ##  Required parameters:
        ##      ip: IP address of SSH daemon.
        ##      username: SSH identity.
        ##      password: SSH key.
        ##      command: The command will run on SSH server.
        ##
        ##  Roger Wei/2021.01.22
        ##
        try:
            SSH_ADDRESS = valueDict['ip']
            SSH_USERNAME = valueDict['username']
            SSH_PASSWORD = valueDict['password']
            SSH_COMMAND = valueDict['command']
        except:
            raise error.nonamevalue()
        
        ## Establish SSH connection ##
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin = ssh_stdout = ssh_stderr = None
        try:
            ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)
        except Exception as e:
            sys.stderr.write("SSH connection error: {0}".format(e))
            raise error.onqaserror()
    
    
    