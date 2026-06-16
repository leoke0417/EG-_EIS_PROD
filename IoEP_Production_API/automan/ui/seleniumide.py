#coding=utf-8
'''
Created on 2010/12/28

@author: panda.huang
'''
import automan.tool.error as error
from automan.tool.verify import Verify
import os,requests
import configparser
config = configparser.ConfigParser()


class seleniumide(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def set(self,browser,value_dict):
        folder = value_dict['folder']
        configfile = value_dict['configfile']
        config.read(os.path.join(os.getcwd() , folder , configfile),encoding="utf-8")
        session = value_dict['session']
        xpath = value_dict['xpath_id']
        #print(config.get('login', xpath))
        elem = browser.find_element_by_xpath(config.get(session, xpath))
        elem.send_keys(value_dict['value'])
    
    def click(self,browser,value_dict):
        folder = value_dict['folder']
        configfile = value_dict['configfile']
        config.read(os.path.join(os.getcwd() , folder , configfile),encoding="utf-8")
        session = value_dict['session']
        xpath = value_dict['xpath_id']
        elem = browser.find_element_by_xpath(config.get(session, xpath))
        elem.click()
    
    def sendkey(self):
        pass