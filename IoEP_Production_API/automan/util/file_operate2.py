#coding=utf-8
"""
Created on 2021/09/01
@author     : Dustin Lin
Project     : Parse json key value
"""
import automan.tool.error as error
import json



class file_operate2(object):
    def __init__(self):  
        pass
    
    def dict_value_get(self, dic_value):
        ## Example:
        ##
        ##
        ##    {
        ##        "xxx": "target_value"
        ##    }
        ## Parameter:
        ##      - response_body
        ##      - key: key of dict.
        ## Result:
        ##      - return type: list

        if 'response_body' and  \
           'key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue() 
                    
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            list_value.append(json_file[dic_value["key"]])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
    
    def dict_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##
        ##    {
        ##        "xxx":{
        ##            "yyy":"target_value"
        ##        }
        ##    }
        ##

        if 'response_body' and \
            'first_key' and \
            'second_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            list_value.append(json_file[dic_value["first_key"]][dic_value["second_key"]])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
            

    def dict_list_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx": [
        ##            "target_value"
        ##        ]
        ##    }
        ##
        ## Parameter:
        ##      - response_body
        ##      - key
        ##  Result:
        ##      - return type: list
        ##
        if 'response_body' and  \
           'key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue() 
            
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["key"]])):
                list_values.append(json_file[dic_value["key"]][i])
            print("\n {} \n".format(list_values))
            return list_values
        except:
            raise error.notfind()
            
    def dict_list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx":"yyy
        ##        "zzz":
        ##            [
        ##                {
        ##                    "target": "target_value1"
        ##                },
        ##                {
        ##                    "target": "target_value2"
        ##                }
        ##            ]
        ##    }
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])            
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]])             
            print("\n {} \n".format(list_values))
            return list_values 
        except:
            raise error.notfind()

    def dict_dict_list_value_get(self, dic_value):
        ## Example:
        ##
        ##{
        ##    "xxx":{
        ##        "yyy":[
        ##            "target_value1",
        ##            "target_value2",
        ##            .
        ##            .
        ##            .
        ##            .
        ##        ]
        ##    }
        ##}
        ##
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ## Result:
        ##      - return type: list
        if 'response_body' and \
            'first_key' and \
            'second_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            list_values = json_file[dic_value["first_key"]][dic_value["second_key"]]
            print("\n {} \n".format(list_values))
            return list_values
        except:
            raise error.notfind()

    def dict_list_dict_list_value_get(self, dic_value):
        ## Example:
        ##
        ##      {
        ##          "xxx":[
        ##                      {
        ##                           "aaa": [
        ##                                      "target_value", "target_value1"    
        ##                                      ]       
        ##                      },...
        ##                  ]
        ##      }
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
            
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                for j in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]])):
                    list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j])
            print("\n {} \n".format(list_values))
            return list_values 
        except:
            raise error.notfind()

    def dict_list_dict_list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx": [
        ##            {
        ##                "yyy":[
        ##                    {
        ##                        "target": "target_value1"
        ##                    },
        ##                    {
        ##                        "target": "target_value2"
        ##                    }
        ##                ]
        ##            }
        ##        ]
        ##    }
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                for j in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]])):
                    list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j][dic_value["third_key"]])
            print("\n {} \n".format(list_values))
            return list_values 
        except:
            raise error.notfind()

        
    def dict_list_dict_dict_list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx": "yyy",
        ##        "zzz": [
        ##             "aaa": {
        ##                    "rrr": [
        ##                            {
        ##                                "target": "target_value"
        ##                            }
        ##                        ]
        ##                }  
        ##            ]
        ##    } 
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ##      - fourth_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' and \
            'fourth_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                for j in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]][dic_value["third_key"]])):
                    list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][dic_value["third_key"]][j][dic_value["fourth_key"]])
            print("\n {} \n".format(list_values))
            return list_values     
        except:
            raise error.notfind()
            
    def dict_list_dict_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx": "yyy",
        ##       "zzz": [
        ##             {
        ##                "eee":{
        ##                    "target": "target_value"
        ##                }
        ##             }
        ##            ]
        ##    }
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
            
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][dic_value["third_key"]])              
            print("\n {} \n".format(list_values))
            return list_values   
        except:
            raise error.notfind()
            
    def dict_dict_dict_list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx": {
        ##            "yyy":{
        ##                "zzz":[
        ##                    {
        ##                        "aaa":"target_value1"
        ##                    },
        ##                    {
        ##                        "aaa":"target_value2"
        ##                    },
        ##                    ...
        ##                ]
        ##            }
        ##        }
        ##    }
        ##
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ##      - fourth_key
        ## Result:
        ##      - return type: list
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' and \
            'fourth_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
           
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]][dic_value["second_key"]][dic_value["third_key"]])):
                list_values.append(json_file[dic_value["first_key"]][dic_value["second_key"]][dic_value["third_key"]][i][dic_value["fourth_key"]])
            print("\n {} \n".format(list_values))
            return list_values
        except:
            raise error.notfind()
         
    def dict_dict_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx":{
        ##            "yyy":{
        ##                "zzz":"target_value"
        ##            }
        ##        }
        ##    }
        ##
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            list_value.append(json_file[dic_value["first_key"]][dic_value["second_key"]][dic_value["third_key"]])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
            
    def dict_dict_list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx":{
        ##            "yyy":[
        ##                {
        ##                    "zzz":"target_value1"
        ##                },
        ##                {
        ##                    "zzz":"target_value2"
        ##                },
        ##                ...
        ##            ]
        ##        }
        ##    }
        ##
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ## Result:
        ##      - return type: list
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]][dic_value["second_key"]])):
                list_values.append(json_file[dic_value["first_key"]][dic_value["second_key"]][i][dic_value["third_key"]])
            print("\n {} \n".format(list_values))
            return list_values 
        except:
            raise error.notfind()
            
    def dict_dict_dict_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    {
        ##        "xxx":{
        ##            "yyy":{
        ##                "zzz":{
        ##                    "aaa": "target_value"
        ##                }
        ##            }
        ##        }
        ##    }
        ##
        ## Parameters:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ##      - fourth_key
        ##
        if 'response_body' and \
            'first_key' and \
            'second_key' and \
            'third_key' and \
            'fourth_key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue()
           
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            list_value.append(json_file[dic_value["first_key"]][dic_value["second_key"]][dic_value["third_key"]][dic_value["fourth_key"]])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
        
    def list_dict_value_get(self, dic_value):
        ## Example:
        ##
        ##    [
        ##        {
        ##            "xxx": "target_value"
        ##            },
        ##        {
        ##            }......
        ##    ]
        ##
        ## Parameters:
        ##      - response_body
        ##      - key
        ##
        if 'response_body' and  \
           'key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue() 
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            for i in range(len(json_file)):
                list_value.append(json_file[i][dic_value["key"]])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
        
    def list_dict_list_value_get(self, dic_value):
        ## Example:
        ##
        ##    [
        ##        {
        ##            "xxx": [
        ##                        "target_value1", "target_value2", ...
        ##                        ]
        ##            },
        ##        {
        ##            }......
        ##    ]
        ##
        ## Parameters:
        ##      - response_body
        ##      - key
        ##
        if 'response_body' and  \
           'key' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue() 
        try:
            json_file = json.loads(dic_value["response_body"])
            list_value = []
            for i in range(len(json_file)):
                for j in range(len(json_file[i][dic_value["key"]])):
                    list_value.append(json_file[i][dic_value["key"]][j])
            print("\n {} \n".format(list_value))
            return list_value
        except:
            raise error.notfind()
        
    
    
    def gateway_device_attributes_get(self, dic_value):
        ## For API: {{qa_end_point}}/api/v1/gateways
        ## ECN:
        ##        attributes:
        ##            1. instanceCode
        ##            2. manufacturerName
        ## BLE:
        ##        attributes:
        ##            1. macAddress
        ## SM:
        ##        attributes:
        ##            1. skin
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                for j in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]])):
                    for k in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j])):
                        if "attributes" in json_file[dic_value["first_key"]][i][dic_value["second_key"]][j].keys():
                            #get value
                            if dic_value["third_key"] in json_file[dic_value["first_key"]][i][dic_value["second_key"]][j]["attributes"]:
                                list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j]["attributes"][dic_value["third_key"]])
                            else:
                                pass
                        else:
                            pass
            print("\n {} \n".format(list_values))
            return list_values     
        except:
            raise error.notfind()
        
    def ioe_audiences_mail_get(self, dic_value):
        ## For API: IoE_GET_hems_post_{id}_audiences_download
        try:
            list_account = dic_value['response_body'].split('\n')
            list_mail = list_account[1:]
            return list_mail
        except:
            raise error.notfind()

    
    def ioe_audiences_column_get(self, dic_value):
        ## For API: IoE_GET_hems_post_{id}_audiences_download
        try:
            list_column = []
            list_account = dic_value['response_body'].split('\n')
            list_column.append(list_account[0])
            return list_column
        except:
            raise error.notfind()

    def list_dict_get(self, dic_value):
        ## Example:
        ##
        ##    [
        ##        {
        ##            'target': 'xxx'
        ##            },
        ##        {
        ##            }......
        ##    ]
        ##
        ## Parameters:
        ##      - response_body
        ##      - key
        ##
        if 'response_body' in dic_value.keys():
            pass
        else:
            raise error.nonamevalue() 
        try:
            json_file = eval(dic_value['response_body'])
            dic_target_onedot = json_file[0]
            print(dic_target_onedot)
            dic_target = str(dic_target_onedot).replace('\'', '"')
            print(dic_target)
            return dic_target
        except:
            raise error.notfind()