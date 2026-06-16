'''
Created on 2015/04/23
@author: Tim.Huang
Description: Open remote desktop console.

Requirement: pip install -U pyautoit
'''
import pyautogui

class Autogui(object):
    def __init__(self):
        pass
    
    def screen_click(self, key):
        pyautogui.click(int(key['x']),int(key['y']))
        
    def screen_size(self):
        print pyautogui.size()