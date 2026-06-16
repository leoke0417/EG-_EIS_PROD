# -*- coding: utf-8 -*-
'''
Created on 2020/05/08

@author: Shawn Lin
'''
import automan.tool.error as error

class ioe_login(object):
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
            dicParm = dict(value_dict)
            objElem = browser.find_element_by_xpath("//input[@name='username']")
            objElem.send_keys(dicParm["key"] )
        except:
            raise error.notfind()
        
    def textbox_password_set(self, browser, value_dict):
        try:
            dicParm = dict(value_dict)
            objElem = browser.find_element_by_xpath("//input[@name='password']")
            objElem.send_keys(dicParm["key"] )
        except:
            raise error.notfind()
        
    def button_login_click(self, browser):
        try:
            objElem = browser.find_element_by_xpath("(//button[@type='button'])[2]")
            objElem.click()
        except:
            raise error.notfind()
        
    def wpage_keyword_verify(self,browser,value_dict):
        try:
            dicParm = dict(value_dict)
            objElem = browser.find_element_by_xpath('//div[@id="app"]/div[2]/div/div/section/div/div/div/div[1]')
            #print(objElem.get_attribute('title'))
            #print(objElem.size)
            #print("objElem.text",objElem.text.encode(encoding='utf-8'))
            """
            except Exception as error:
                print(error)
            """
        except:
            raise error.notfind()
            
        