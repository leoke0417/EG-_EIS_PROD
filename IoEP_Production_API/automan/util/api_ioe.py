#coding=utf-8
"""
Created on 2021/05/07
@author     : Dustin Lin
Project     : Postman Automan Integration
"""
import automan.tool.error as error  
from automan.tool.verify import Verify
import configparser
import subprocess
import botocore
from botocore import UNSIGNED
from warrant.aws_srp import AWSSRP
import boto3
import time
import json
import csv
import sys
import os
import re

class api_ioe(object):
    def __init__(self):  
        pass
    
        
    def refresh_token_body_get(self, dic_value):
        ## In order to setup the request body
        ## Due to the token will refresh every 8 hours
        ## 
        ## Required parameters:
        ##      access_token
        ##      refresh_token
        ##
        try:
            dic_value["access_token"] in locals().keys()
            dic_value["refresh_token"] in locals().keys()
        except:
            raise error.nonamevalue()
            
        try:
            access_token = eval(dic_value["access_token"])
            access_token = access_token[0]
            refresh_token = eval(dic_value["refresh_token"])
            refresh_token = refresh_token[0]
            body = "{\"accessToken\": \"" + access_token + "\"," + \
                    "\"refreshToken\": \"" + refresh_token + "\"}"
        except:
            raise error.notfind()
        return body
        
    def refresh_token_new_body_get(self, dic_value):
        ## To change a new request body which generated from the func.(refresh_token_body_get)
        ##
        ## Required parameters:
        ##      collection_content
        ##      new_body
        ##
        try:
            dic_value["collection_content"] in locals().keys()
            dic_value["new_body"] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            json_content = json.loads(dic_value["collection_content"])
            json_content["item"][0]["request"]["body"]["raw"] = dic_value["new_body"]
            # length of json_content = 2
            # json_content["item"][0] ==> Testcase: get_token
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file
        
    def users_devices_get(self, dic_value):
        ## Purpose:
        ##      For API Get /hems/user-accounts
        ##      In order to get devices model and onlineStatus
        ##      Due to there are some gateways have no devices
        ##      Need to check if there are some devices associated to the gateway       
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
        try:
            dic_value["response_body"] in locals().keys()
            dic_value["first_key"] in locals().keys()
            dic_value["second_key"] in locals().keys()
            dic_value["third_key"] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            json_file = json.loads(dic_value["response_body"])
            list_values = []
            for i in range(len(json_file[dic_value["first_key"]])):
                for j in range(len(json_file[dic_value["first_key"]][i][dic_value["second_key"]])):
                    if len(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j]) == 0:
                        print("No devices")
                        pass
                    else:
                        list_values.append(json_file[dic_value["first_key"]][i][dic_value["second_key"]][j][dic_value["third_key"]])
            print("\n {} \n".format(list_values))
            return list_values 
        except:
            raise error.notfind()
        
        
    def update_post_new_id_get(self, dic_value):
        ## for PUT, DELETE app-labels
        ## add uuid to url
        ##
        ## Required parameters
        ##      collection_content
        ##      app_label_uuid
        ##
        try:
            dic_value["collections"] in locals().keys()
            dic_value["new_id"] in locals().keys()
            tuple_new_param = eval(dic_value["new_id"])
        except:
            raise error.nonamevalue()
        try:
            json_content = json.loads(dic_value["collections"])
            json_content["item"][0]["request"]["url"]["raw"] = tuple_new_param[0]
            json_content["item"][0]["request"]["url"]["path"] = tuple_new_param[1]
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file

    
    def update_post_id_url_get(self, dic_value):
        ## To generate new url 
        ##
        ## Required parameters
        ##      app_label_uuid
        ##
        try:
            dic_value["id_url"] in locals().keys()
            idd = eval(dic_value["id_url"])
        except:
            raise error.nonamevalue()
        
        
        try:
            url = "{{qa_end_point}}/hems/posts/" + idd[0]
            path = ["hems","posts",idd[0]]
        except:
            raise error.notfind()
        
        return url,path
        

    def update_devices_uuid_get(self, dic_value):
        ## To generate new url 
        ##
        ## Required parameters
        ##      app_label_uuid
        ##
        ## use to change the uuid for delete API after pair smartMeter
        try:
            dic_value["devices_uuid"] in locals().keys()
            uudd = eval(dic_value["devices_uuid"])
        except:
            raise error.nonamevalue()
        
        
        try:
            url = "{{qa_end_point}}/api/v1/associations/devices/" + uudd[0]
            path = ["api", "v1", "associations", "devices",uudd[0]]
        except:
            raise error.notfind()
        
        return url,path
    
    def update_images_path_get(self, dic_value):
        
        try:
            dic_value["path"] in locals().keys()
            
        except:
            raise error.nonamevalue()
        
        json_content = json.loads(dic_value["path"])
        json_url=os.path.join(os.getcwd(),'ini','API_NextDrive','uploaded_file','IoE','API_test_sample.png')
        json_url.replace('\\','/')
        json_url='/'+json_url
        json_content['item'][0]["request"]["body"]["formdata"][0]["src"]=json_url
        json_file = json.dumps(json_content)
          
        
        return json_file
        
        
        
            