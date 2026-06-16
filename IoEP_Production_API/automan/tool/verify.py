#coding:utf-8
'''
Created on 2011/1/11

@author: panda109
'''
import automan.tool.error as error

class Verify(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def verify(self,local_dict):
        if 'criteria' in local_dict:
            if local_dict['criteria'] == '=':
                if local_dict['system_value'] == local_dict['value']:
                    pass
                else:
                    print ("verify string dict : ") , local_dict
                    raise error.equalerror()
            if local_dict['criteria'] == '!':
                if local_dict['system_value'] != local_dict['value']:
                    pass
                else:
                    print ("verify string dict : ") , local_dict
                    raise error.notequalerror()
        else:
            raise error.nonamevalue()