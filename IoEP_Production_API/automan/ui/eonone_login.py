#coding=utf-8
'''
Created on 2015/04/28

@author: Jason Ma
'''
import time
import automan.tool.error as error
from selenium.webdriver.common.keys import Keys
from automan.util.tool  import Tool
from selenium.webdriver.common.by import By
import os
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini' , "Eonone.conf"),encoding="utf-8")


class eonone_login(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass


    def textbox_username_set(self, browser, value_dict):
        try:
            local_dict = dict(value_dict)
            elem = browser.find_element_by_id(config.get("login", "id_signin_username"))
            elem.send_keys(local_dict["key"] )
        except:
            raise error.notfind()
        
    def textbox_password_set(self, browser, value_dict):
        try:
            local_dict = dict(value_dict)
            elem = browser.find_element_by_id(config.get("login", "id_signin_passwd"))
            elem.send_keys(local_dict["key"] )    
        except:
            raise error.notfind()
        
    def button_login_click(self, browser):
        try:
            text = config.get("login", "class_signin_button")
            xpath="//button[@class='replace']"
            elem = browser.find_element_by_xpath(xpath.replace("replace",text))
            elem.click()
        except:
            raise error.notfind()