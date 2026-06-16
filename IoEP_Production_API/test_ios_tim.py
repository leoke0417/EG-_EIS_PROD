'''
Created on 2011/2/14

@author: panda109
'''
import time
from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait



class test_web(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    if __name__ == '__main__':
        command_executor = "http://127.0.0.1:4723/wd/hub"
        app_path = '/Users/lawrey/Library/Developer/Xcode/DerivedData/AppiumTest-fubxvjmcpxiewkenopxpcerwhudw/Build/Products/Debug-iphonesimulator/AppiumTest.app'
        
       
        dc = {
  "platformName": "iOS",
  "platformVersion": "13.5.1",
  "deviceName": "黃文銘 的 iPhone",
  "automationName": "XCUITest",
  "app": "/Users/tim/Library/Developer/Xcode/DerivedData/UIKitCatalog-airxbtmaaptlqxerqpkmkbeizjzg/Build/Products/Debug-iphoneos/UIKitCatalog.app",
  "udid": "765fa19750958c0f48ba2f666df59f81b7b8bdbb"
}
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=dc)
        #screenshotBase64 = driver.get_screenshot_as_base64()
        driver.save_screenshot('./log/test.png')
        #el = driver.find_element_by_id('android:id/text1')
        #el.click()
        driver.quit()
        
        