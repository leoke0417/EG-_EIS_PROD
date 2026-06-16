'''
Created on 2011/2/14

@author: panda109
'''
import time
from appium import webdriver

class test_web(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    if __name__ == '__main__':
        dc = {}
        dc['platformName'] = 'Android'
        dc['deviceName'] = 'GCNPCX025651GHH'
        dc['platformVersion'] = '7'
        dc['noReset'] = True
        dc['app'] = "c:\\Android\\ApiDemos-debug.apk"
        dc['autoAcceptAlerts'] = True

        driver = webdriver.Remote('http://127.0.0.1:4725/wd/hub', desired_capabilities=dc)
        el = driver.find_element_by_id('android:id/text1')
        el.click()
        driver.quit()
        
        