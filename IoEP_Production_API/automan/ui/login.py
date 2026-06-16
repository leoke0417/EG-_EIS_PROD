#coding:utf-8
'''
Created on 2015/04/28

@author: Jason Ma
'''
import time
import automan.tool.error as error
from selenium.webdriver.common.keys import Keys
from automan.util.tool  import Tool
import configparser
import os
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini' , "Path.conf"),encoding="utf-8")

class login(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass


    def textbox_username_set(self, browser, value_dict):
        local_dict = dict(value_dict)
        elem = browser.find_element_by_id(config.get("login", "id_signin_username"))
        elem.send_keys(local_dict["key"] )

    def textbox_password_set(self, browser, value_dict):
        local_dict = dict(value_dict)
        elem = browser.find_element_by_id(config.get("login", "id_signin_passwd"))
        elem.send_keys(local_dict["key"] )

    def button_signin_click(self, browser):
        elem = browser.find_element_by_id(config.get("login", "id_signin_button"))
        elem.click()

    #====verify login sucess
    def login_success_verify(self, browser, value_dict): 
        local_dict = dict(value_dict)
        try:
            browser.find_element_by_link_text(config.get("login", "login_verify")).text
            verify_vaule = 'success'
        except:
            verify_vaule = 'Fail'       
        local_dict['value'] = verify_vaule
        print (local_dict)
        Tool().dir_verify(local_dict)
       