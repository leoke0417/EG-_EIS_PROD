#coding:utf-8
'''
Created on 2010/12/15

@author: panda.huang
'''
from selenium import webdriver
from appium import webdriver as appium
from automan.tool.parse_file import Parse_file
import os
import platform
class Browser(object):
    '''
    classdocs
    '''
    
    def __init__(self,param,browser):
        if browser  == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")   #chrom browser maximization
            #options.add_argument("-incognito")  #open in incognito mode
            #enable multiple download
            #multi_dl_prefs = {}
            #multi_dl_prefs['profile.default_content_settings.multiple-automatic-downloads'] = 1
            #options.add_experimental_option("prefs", multi_dl_prefs)
            if platform.system() == 'Darwin' :             
                driver_path = os.getcwd() + '/chromedriver'
            else: 
                driver_path = os.getcwd() + '/chromedriver.exe'
            self.browser = webdriver.Chrome(driver_path , chrome_options=options)
                
            self.browser.get(param)

        if browser == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.privatebrowsing.autostart", True)
            self.browser = webdriver.Firefox(firefox_profile=profile)
            self.browser.maximize_window()   
            self.browser.get(param)

        ##if browser == "ie":
        #    self.browser = webdriver.Browser()
        #    self.browser.maximize_window()            
        #    #print self.driver.get_window_size()
        #    self.browser.get(param)

        if browser == "app":
            #read from url in to desired_capabilities
            dc = {}
            app = Parse_file().get_app(param)
            for line in list(app):
                if str(line).strip().split('=')[1] == 'True':
                    dc[str(line).strip().split('=')[0]] = True
                else:
                    dc[str(line).strip().split('=')[0]] = str(line).strip().split('=')[1]
            self.browser = appium.Remote('http://127.0.0.1:%s/wd/hub' % dc['port'], desired_capabilities=dc)
            