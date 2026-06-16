#coding:utf-8
'''
Created on 2010/12/10
@author: panda.huang
'''
import automan.tool.error as error
from selenium.webdriver.common.keys import Keys
import configparser
import os
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'conf' , "test.conf"),encoding="utf-8")

class google(object):
    '''
    classdocs
    '''
    def __init__(self):
        pass
   
    def set(self,browser,value_dict):
        xpath = value_dict['xpath_id']
        print(xpath)
        elem = browser.find_element_by_xpath(config.get('test', xpath))
        elem.send_keys(value_dict['value'])
    
    def click(self,browser,value_dict):
        xpath = value_dict['xpath_id']
        elem = browser.find_element_by_xpath(config.get('test', xpath))
        elem.click()

    #===========================================================================
    # def textbox_search_set(self,browser,value_dict):
    #     local_dict = dict(value_dict)
    #     elem = browser.find_element_by_name('q')
    #     elem.send_keys(local_dict["key"])
    #     elem.send_keys("中".decode('utf-8'))
    #===========================================================================


    def search_new_2_set(self,browser,value_dict):
        
        xpath = value_dict['xpath_id']
        print(xpath)
        elem = browser.find_element_by_xpath(config.get('test', xpath))
        elem.send_keys(value_dict['value'])
    
    def button_submit_2_click(self,browser,value_dict):
        
        xpath = value_dict['xpath_id']
        elem = browser.find_element_by_xpath(config.get('test', xpath))
        elem.click()

        
    def button_search_send(self,browser):
        elem = browser.find_element_by_name('q')
        elem.send_keys(Keys.RETURN)

    def button_error_send(self,browser):
        return 1
    
    def text_gmail_print(self,browser):
        elem = browser.find_element_by_class_name('gb_g')
        print(elem.text)
