'''
Created on 2010/12/28

@author: panda.huang
'''
import hashlib
import automan.tool.error as error
import os
import subprocess                 
from automan.tool.verify import Verify

class File(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def shellcmd_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1
        
    def shellcmd_get(self,dict):
        
        ret=self.shellcmd_output(dict['command'])
        return ret      
    def rdfolder_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1
        
    def mdfolder_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1    
    
    def smbnetuse_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1

    def copy_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1

    def download_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1

    def clean_exec(self,dict):
        try:
            os.system(dict['command'])
            return 0
        except:
            return 1

    def getmd5_get(self,dict):
        hash_md5 = hashlib.md5()
        with open(dict['file'], "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    
    def equalmd5_verify(self,dict):
        if (dict['md5'] == dict['ldmd5']):
            return 0
        else:
            raise error.notequalerror()
    
    def shellcmd_output(self,command):
        #store stdout to tempfile
        fTemp="temp.stdout"
        #print (dict['command'])
        if os.path.isfile(os.path.join(os.getcwd(),fTemp)):
           os.remove(os.path.join(os.getcwd(),fTemp))
        
        #try:
        subprocess.run(command + " > " + fTemp, shell=True, capture_output=True)
        for line in open(os.path.join(os.getcwd(),fTemp)):
               print(str(line))
               return str(line)
            #return 0
        #except:
        return 1 