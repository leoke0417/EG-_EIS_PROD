# _*_ coding:utf-8 _*_
'''
Created on 2015/04/23
@author: Jack.Lin
Description: Open remote desktop console.

Requirement: pip install -U pyautoit
'''
from pyVim import connect
import ssl
import automan.tool.error as error
class Pyvmomi(object):
    def __init__(self):
        '''
        Constructor
        '''
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.verify_mode = ssl.CERT_NONE
    
    def instance_check(self,dict):
        self.ci = connect.SmartConnect(host=dict['ip'],user=dict['user'],pwd=dict['password'],port=int(dict['port']),sslContext=self.context)
        datacenter = self.ci.content.rootFolder.childEntity[0]
        vms = datacenter.vmFolder.childEntity
        self.tagvm = 0
        for i in vms:
            if (i.name == dict['vmname']):
                self.tagvm = 1
        if (self.tagvm == 0):
            raise error.nonamevalue()
    def __del__(self):
        connect.Disconnect(self.ci)