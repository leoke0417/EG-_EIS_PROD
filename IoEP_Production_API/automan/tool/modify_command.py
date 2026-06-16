#coding:utf-8
'''
Created on 2010/12/17

@author: panda.huang
'''

class Modify_command(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def replay_ini(self,systemini,currentyini,command):
        list_command=[]
        list_command = str(command).strip().split('$')
        for index in range(len(list_command)):
            if list_command[index] in currentyini:
                list_command[index] = currentyini[list_command[index]]
            if list_command[index] in systemini:
                list_command[index] = systemini[list_command[index]]
        print ('parameters => '+''.join(list_command))
        return ''.join(list_command)
    
    
    