'''
Created on 2015/04/23
@author: Jack.Lin
Description: Open remote desktop console.

Requirement: pip install -U pyautoit
'''
import os
import win32com.client

class Autoit(object):
    def __init__(self):
        self.autoit = win32com.client.Dispatch("AutoItX3.Control")
        
    def app_run(self, key):
        #print key['name']
        self.autoit.Run(key['name'])

    def app_dosrun(self, key):
        #print key['name']
        os.system(key['name'])

    def control_click(self, key):
        self.autoit.ControlClick(key['title'], "", key['value'])

    def app_close(self):
        self.autoit.Send("!{F4}")