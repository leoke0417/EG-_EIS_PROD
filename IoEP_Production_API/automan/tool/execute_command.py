#coding:utf-8
'''
Created on 2010/12/10

@author: panda.huang
'''
import time
from automan.tool.parse_file import Parse_file
from automan.tool.userclass import Userclass
from automan.tool.modify_command import Modify_command
from automan.tool.parse_name_value import Parse_name_value
import automan.tool.error as error
from automan.ui.browser import Browser


class Execute_command(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.userclass = Userclass()
        self.currentlyini = {'debug' : 'off'}
        self.namevalue = {}
        '''
        Constructor
        '''
   
    def execute(self, command, systemini):
        result = 0
        ret = 0
        #print("command",command)
        #print("systemini",systemini)
        if self.currentlyini['debug'] == 'on':
            print (systemini)
            print (self.currentlyini)
        #need to be merge into userclass
        if len(command) >= 3 and str(command[2]) == 'browser':
            from automan.ui.browser import Browser
        if len(command) >= 4 and str(command[2]) != 'browser':
            self.userclass.check_class(command[2])
        try:
            if list(command).__len__() == 2:
                if command[1] == 'end':
                    try:
                        if self.browser:
                            self.browser.quit()
                    except:
                        pass
            elif list(command).__len__() == 3:
                if command[1] == 'ini':                   
                   self.currentlyini.update(Parse_file().get_ini(str(command[2])))
                elif command[1] == 'sleep':
                    time.sleep(int(command[2]))
                elif command[1] == 'debug' and command[2] == 'on':
                    self.currentlyini.update({'debug':'on'})
                elif command[1] == 'debug' and command[2] == 'off':
                    self.currentlyini.update({'debug':'off'})
                elif command[1] == 'close' and command[2] == 'browser':
                    try:
                        if self.browser:
                            self.browser.quit()
                    except:
                        pass
            elif list(command).__len__() == 4:
                if command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "chrome":
                   self.browser = Browser(systemini['chrome'],command[3].lower()).browser
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "firefox":
                    self.browser = Browser(systemini['firefox'],command[3].lower()).browser
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "ie":
                    self.browser = Browser(systemini['ie'],command[3].lower()).browser
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "app":
                    self.browser = Browser(systemini['app_device'],command[3].lower()).browser       
                else:
                    #print (command)
                    ob = self.userclass.class_object[self.get_objectname(command)]
                    defname = self.get_defname(systemini,command)
                    ret = eval(defname)
                    if ret == 1 :
                        self.browser.save_screenshot('./log/app.png')
            elif list(command).__len__() == 5:
                if command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "chrome":
                   self.browser = self.Browser(systemini[command[4].lower()],command[3].lower()).brower
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "firefox":
                    self.browser = Browser(systemini[command[4].lower()],command[3].lower()).browser
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "ie":
                    self.browser = Browser(systemini[command[4].lower()],command[3].lower()).browser
                elif command[1] == 'init' and command[2] == 'browser' and command[3].lower() == "app":
                    self.browser = Browser(systemini['app_device'],command[3].lower()).browser
                else:
                    ob = self.userclass.class_object[self.get_objectname(command)]
                    defname = self.get_defname(systemini,command)
                    #print (defname)
                    ret = eval(defname)
                    if ret == 1 :
                        self.browser.save_screenshot('./log/app.png')        
            elif list(command).__len__() == 6:
                pass
            if str(command[1]).find('$=get')>0:
                print(ret)
                self.modify_currentlyini(command[1], ret)
                ret = 0
        except error.nonamevalue:
            print ("FAIL !! no name or key is in param_dict")
            ret = 1
        except error.equalerror:
            print ("FAIL !! value is not equal or exist")
            ret = 1
        except error.notequalerror:
            print ("FAIL !! value is equal or exist")
            ret = 1
        except error.notfind:
            print ("FAIL !! not find")
            ret = 1    
        except error.find:
            print ("FAIL !! find")
            ret = 1    

        #except:
        #    result = 1
        if ret == None:
            return 0
        else:
            return ret
    
    def get_objectname(self,command):
        
        if str(command[2]).find('browser.')==0:
            #print (str(str(command[2]).split('.')[1]).lower())
            return str(str(command[2]).split('.')[1]).lower()
        else:
            return str(command[2]).lower()
        
    def get_defname(self,systemini,command):
        
        if str(command[1]).find('=') > 0:
            action = str(str(command[1]).split('=')[1]).strip()
        else:
            action = command[1]
            
        if action == '~click':
            function_name = 'click'
        elif action == '~set':
            function_name = 'set'
        else:
            function_name = command[3] + '_' + action
        
        if list(command).__len__() == 4:
            if str(command[2]).find('browser.')==0:
                return 'ob.' + function_name + '(self.browser)'
            else:
                return 'ob.' + function_name + '()'
        elif list(command).__len__() == 5:
            param = Modify_command().replay_ini(systemini, self.currentlyini,str(command[4]))
            self.namevalue = Parse_name_value().parse_name_value(param)
            if str(command[2]).find('browser.')==0:
                return 'ob.' + function_name + '(self.browser,self.namevalue)'
            else:
                return 'ob.' + function_name + '('+'self.namevalue'+')'   
            
    def modify_currentlyini(self,key,value):
        #print (key)
        #print (value)
        self.currentlyini[str(key).split('$')[1]]=str(value)
