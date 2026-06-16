# _*_ coding:utf-8 _*_
'''
Created on 2015/04/23
@author: Jack.Lin
Description: Open remote desktop console.

Requirement: pip install -U pyautoit
'''

import jpype  
from jpype import *  
from pickle import NONE
import automan.tool.error as error
#from _overlapped import NULL

class Sikuli(object):
    def __init__(self):
        '''
        Constructor
        '''
        jvmPath = getDefaultJVMPath()
        jpype.startJVM(jvmPath, '-ea', r'-Djava.class.path=sikulixapi_mac.jar' , convertStrings=False)
        #self.app = JClass('org.sikuli.script.App')
        Screen = JClass('org.sikuli.script.Screen')
        self.screen = Screen()

    def icon_click(self, name):
        try:
            if self.screen.exists(name['key']):
                self.screen.click(name['key'])
            else:
                raise error.notfind()
        except :
            raise error.notfind()
            
    def text_type(self,text):
        try:
            self.screen.type(text['value'])
        except:
            raise error.notfind()
        
    def enter_type(self):
        try:
            self.screen.type("\n")
        except:
            raise error.notfind()
                
    def __del__(self):
        shutdownJVM()

