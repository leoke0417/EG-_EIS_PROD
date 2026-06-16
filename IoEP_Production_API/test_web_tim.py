'''
Created on 2011/2/14

@author: panda109
'''
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class test_web(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    if __name__ == '__main__':
        #driver = webdriver.Chrome() aaa
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9015")
        chrome_driver = "C:\python\chromedriver.exe"
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        print(driver.title)

        #driver.close()
        #Browser(systemini['firefox'],command[3].lower()).browser
        #driver.get('https://ioe-staging.nextdrive.io/')
        #driver.get('http://google.com')
        #url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
        
        #session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
        
        
        #driver = webdriver.Remote(command_executor=url,desired_capabilities={})
        #driver.close()   # this prevents the dummy browser
        
        
        #time.sleep(20)
        #driver.session_id = session_id
        #driver.get("http://www.mrsmart.in")
        #time.sleep(20)
        # 
        # objElem = driver.find_element_by_xpath("//input[@name='username']")
        # objElem.send_keys("shawn.lin@nextdrive.io")
        # objElem = driver.find_element_by_xpath("//input[@name='password']")
        # objElem.send_keys("1q2w3E4R" )
        # objElem = driver.find_element_by_xpath("(//button[@type='button'])[2]")
        # objElem.click()
        #=======================================================================
              
        #time.sleep(5)       
        #objElem = driver.find_element_by_xpath('//div[@id="app"]/div[2]/div/div/section/div/div/div/div[1]')
        #print(objElem.text.encode(encoding='UTF-8'))

        #driver.get("http://www.python.org")
        #elem = driver.find_element_by_name('q')
        #elem.send_keys("pycon")
        #elem.send_keys(Keys.RETURN)
        #for handle in driver.window_handles:
        #    print "Handle = ",handle
        #driver.close()