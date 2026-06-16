# _*_ coding:utf-8 _*_
'''
Created on 2015/04/23
@author: Jack.Lin
Description: Open remote desktop console.

Requirement: pip install -U pyautoit
'''

import jpype  
from jpype import *  
import automan.tool.error as error


def main():
    #try:
    jvmpath=jpype.getDefaultJVMPath()
    #启动jvm
    jpype.startJVM(jvmpath, '-ea', r'-Djava.class.path=sikulixapi_mac.jar', convertStrings=False)
    Screen = jpype.JClass('org.sikuli.script.Screen')
    screen = Screen()
    #打印
    #jpype.java.lang.System.out.println("dsfsfsfds")
    #关闭jvm
    screen.close()
    jpype.shutdownJVM()
    
    
        #jvmPath = getDefaultJVMPath()
        #jpype.startJVM(jvmPath, '-ea', r'-Djava.class.path=sikulixapi_mac.jar' , convertStrings=False)
        #app = jpype.JClass('org.sikuli.script.App')
        #app =JClass('org.sikuli.script.App')
       # Sikuli = jpype.JPackage("org.sikuli.script")
        #screen = Sikuli.Screen()
        
        #Screen = jpype.JClass('org.sikuli.script.Screen')
        
        #Key = JClass('org.sikuli.script.Key')
        #self.screen = Screen.
        #self.app = JClass('org.sikuli.script.App')
        
        #screen = Screen()
        
        #x = screen.exists('./img/HCI/ip.png')
        #print (x)
    #except:
    #3        print ("FAIL")
        #shutdownJVM()

if __name__ == '__main__':
    main()
        

