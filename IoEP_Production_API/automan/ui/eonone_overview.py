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
from selenium.webdriver.common.action_chains import ActionChains
import os
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini') + "Eonone.conf",encoding="utf-8")


class eonone_overview(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass

    def sharefolder_click(self, browser):
        try:
            text = config.get("overview", "class_sharefolder")
            xpath="//div[@class='replace']"
            elem = browser.find_element_by_xpath(xpath.replace("replace",text))
            Hover = ActionChains(browser).move_to_element(elem)
            Hover.click().perform()
            #print elem.text
        except:
            raise error.notfind()
