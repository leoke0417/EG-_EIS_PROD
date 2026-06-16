# -*- coding: utf-8 -*-
'''
Created on 2020/05/08

@author: Shawn Lin
'''
import automan.tool.error as error
import configparser,os.path
from _operator import sub

objConfig = configparser.ConfigParser()
objConfig.read(os.path.join(os.getcwd(), 'ini', 'EcoTrans',"EcoTrans.conf"))


class web_main(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
    
    def button_lang_click(self, browser, value_dict):
        try:
            dicParm = dict(value_dict)
            """
            objElem = browser.find_element_by_class_name("el-dropdown-menu el-popper")        
            objElem.click()
            time.sleep(3)
            """
            #objElem = browser.find_element_by_xpath(objConfig['web'][dicParm['xpath']])
            objElem = browser.find_element_by_xpath("//*[contains(text(), %s)]" % dicParm['lang'])
            objElem.click()
            
        except Exception as strError:
            #raise error.notfind()
            print('error',strError)
    
    def textbox_set(self, browser, value_dict):
        try:
            dicParm = dict(value_dict)
            #objElem = browser.find_element_by_xpath(objConfig['web'][dicParm['xpath']])
            objElem = browser.find_element_by_xpath(objConfig.get("web", dicParm["xpath"]))
            objElem.send_keys(dicParm["key"] )
        except:
            raise error.notfind()
        
    def button_click(self, browser, value_dict):
        try:
            dicParm = dict(value_dict)
            #objElem = browser.find_element_by_xpath(objConfig['web'][dicParm['xpath']])
            objElem = browser.find_element_by_xpath(objConfig.get("web", dicParm["xpath"]))
            objElem.click()
        except:
            raise error.notfind()
            
    def wpage_keyword_verify(self,browser,value_dict):
        try:
            dicParm = dict(value_dict)
            objElem = browser.find_element_by_xpath(objConfig['web'][dicParm['xpath']])
            #print(objElem.get_attribute('title'))
            #print(objElem.size)
            #print("objElem.text",objElem.text.encode(encoding='utf-8'))
            """
            except Exception as error:
                print(error)
            """
        except:
            raise error.notfind()
    def url_set(self, browser, value_dict):
        browser.get(value_dict["url"])
        
    def element_verify(self, browser, dicValue):
        dicParm = dict(dicValue)
        try:
            element_on_screen = browser.find_element_by_xpath(objConfig['web'][dicParm['xpath']])
            #element_on_screen.click()
        except:
            raise error.notfind()
            
        