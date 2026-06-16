#coding:utf-8
'''
Created on 2010/12/10
@author: panda.huang
'''
import automan.tool.error as error

class asus(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass
    def textbox_search_click(self,browser,value_dict):
        el = browser.find_element_by_id('android:id/text1')
        el.click()
        
    def page_back(self,browser):
        browser.back()

    def error_test(self,browser):
        return 1