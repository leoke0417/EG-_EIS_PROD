#coding:utf-8
'''
Created on 2010/12/28

@author: panda.huang
'''

class Userclass(object):
    '''
    classdocs
    '''


    def __init__(self):
        
        self.class_object = {}
        '''
        Constructor
        '''
    
    def check_class(self,command):
        #print (command)
        if str(command).find('.')>=0:
            keyname = str(str(command).split('.')[1]).lower()
            classname = str(command).split('.')[1]
            cmd = 'from automan.ui.' + keyname +' import ' + classname
        else:
            keyname = str(str(command)).lower()
            classname = str(command)
            cmd = 'from automan.util.' + keyname +' import ' + classname
            
        if  keyname in self.class_object.keys():
            pass
        else:
            #print(cmd)
            exec( cmd )
            self.class_object[keyname] = eval(classname+'()')
        #print self.class_object
        
