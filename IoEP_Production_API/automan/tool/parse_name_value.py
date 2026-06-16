#coding:utf-8
'''
Created on 2010/12/28

@author: panda.huang
'''

class Parse_name_value(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def parse_name_value(self,name_value):
        namevalue = {}
        # no key or name
        if str(name_value).count('#') == 0 :
            namevalue['default'] = str(name_value)
        else: 
        # 1234 -> {'default': '1234'}
        # #key# = 1234 -> {'key': '1234'}
        # #name# = test , #value# = 100 , #key# = , #criteria# = equal -> {'value': '100', 'system_value': 'test1', 'name': 'test', 'key': '', 'criteria': 'equal'}
            for name_vale_list in str(name_value).split(',#'):
                name = str(name_vale_list.strip()).split('=')[0]
                if str(name_vale_list.strip()).count('=') == 1:
                    if str(name_vale_list.strip()).split('=')[1] == '' and len(str(name_vale_list.strip()).split('=')) == 2:
                        value = ' '
                    elif len(str(name_vale_list.strip()).split('=')) == 3: 
                        value = '='
                    else:
                        value = str(name_vale_list.strip()).split('=')[1].strip()
                else:
                    value = str(name_vale_list.strip().split('#=')[1]).strip()
                name = str(name).replace("#", "")
                namevalue[name.strip()] = value
        return namevalue
    
    
    
    
