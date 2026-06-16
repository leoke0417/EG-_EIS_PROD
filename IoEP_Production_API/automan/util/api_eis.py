#coding=utf-8
"""
Created on 2021/05/06
@author     : Dustin Lin
Project     : Postman Automan Integration
"""
import automan.tool.error as error  
from automan.tool.verify import Verify
import configparser
import subprocess
import botocore
from botocore import UNSIGNED
# from warrant.aws_srp import AWSSRP
from warrant_lite import WarrantLite as AWSSRP
import boto3
import time
import json
import csv
import sys
import os
import re

class api_eis(object):
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
            body = "{\"access_token\": \"" + access_token + "\"," + \
                    "\"refresh_token\": \"" + refresh_token + "\"}"
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
            json_content["item"][1]["request"]["body"]["raw"] = dic_value["new_body"]
            # length of json_content = 2
            # json_content["item"][0] ==> Testcase: get_token
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file
        
    def create_organizations_body_get(self, dic_value):
        ## To create a new request body for create organization
        ## API: POST /organizations
        ## Required parameters:
        ##      country
        ##      industry
        ##      account_manager
        try:
            dic_value["country"] in locals().keys()
            dic_value["industry"] in locals().keys()
            dic_value["account_manager"] in locals().keys()
            org_name = "API_Created_" + str(int(time.time()))
        except:
            raise error.nonamevalue()
        
        try:
            body = "{\"name\": \"" + org_name + "\", " + \
                    "\"country\": \"" + dic_value["country"] + "\"," + \
                    "\"industry\": \"" + dic_value["industry"] + "\"," + \
                    "\"accountManager\": \""+ dic_value["account_manager"] + "\"}"
        except:
            raise error.notfind()
        
        return body
    
    def create_organizations_new_body_get(self, dic_value):
        ## To change a new request body which generated from the func.(create_organizations_body_get)
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
            json_content["item"][1]["request"]["body"]["raw"] = dic_value["new_body"]
            # length of json_content = 2
            # json_content["item"][0] ==> Testcase: get_token
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file
            
    def create_clients_body_get(self, dic_value):
        ## To create a new body for create client
        ## API: POST /clients
        ##
        ## Required parameters:
        ##      location
        ##      type
        ##      account_manager
        ##      organization_id
        ##
        try:
            dic_value["location"] in locals().keys()
            dic_value["type"] in locals().keys()
            dic_value["account_manager"] in locals().keys()
            dic_value["organization_id"] in locals().keys()
            client_name = "API_Created_" + str(int(time.time()))
        except:
            raise error.nonamevalue()
            
        try:
            organization_id = eval(dic_value["organization_id"])
            organization_id = organization_id[0]
            body = "{\"name\": \"" + client_name + "\"," + \
                    "\"location\": \"" + dic_value["location"] + "\"," + \
                    "\"type\": \"" + dic_value["type"] + "\"," + \
                    "\"accountManager\": \"" + dic_value["account_manager"] + "\"," + \
                    "\"organizationId\": \"" + organization_id + "\"}"
        except:
            raise error.notfind()
            
        return body
              
    def create_clients_new_body_get(self, dic_value):
        ## To change a new request body which generated from the func.(create_organizations_body_get)
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
            json_content["item"][1]["request"]["body"]["raw"] = dic_value["new_body"]
            # length of json_content = 2
            # json_content["item"][0] ==> Testcase: get_token
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file
        
    def create_programs_body_get(self, dic_value):
        ## To create a new body for create program
        ## API: POST /programs
        ##
        ## Required parameters:
        ##      client_id
        ##      account_manager
        ##
        try:
            dic_value["client_id"] in locals().keys()
            dic_value["account_manager"] in locals().keys()
            start_date = time.strftime("%Y%m%d", time.gmtime())
            program_name = "API_Created_" + str(int(time.time()))
        except:
            raise error.nonamevalue()
            

        client_id = eval(dic_value["client_id"])
        client_id = client_id[0]
        print(client_id)
        print(type(client_id))
        print(dic_value["account_manager"])
        print(type(dic_value["account_manager"]))
        body = "{\"client\": " + str(client_id) + "," + \
                "\"title\": \"" + program_name + "\"," + \
                "\"country\": \"JP\"," + \
                "\"type\": \"Others\"," + \
                "\"period\": 3," + \
                "\"startDate\": \"" + start_date + "\"," + \
                "\"countingDate\": \"5\"," + \
                "\"accountManager\": \"" + dic_value["account_manager"] + "\"," + \
                "\"products\":[{\"type\":\"HEMS\",\"plan\":\"Standard\",\"fwFeature\":\"ECHONET_LITE\",\"availableDevices\":[],\"licenseLimit\":5}]}"
        print(body)
        
        return body
        
    def create_programs_new_body_get(self, dic_value):
        ## To change a new request body which generated from the func.(create_organizations_body_get)
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
            json_content["item"][1]["request"]["body"]["raw"] = dic_value["new_body"]
            # length of json_content = 2
            # json_content["item"][0] ==> Testcase: get_token
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file



    def update_app_labels_url_get(self, dic_value):
        ## To generate new url 
        ##
        ## Required parameters
        ##      app_label_uuid
        ##
        try:
            dic_value["app_label_uuid"] in locals().keys()
            app_label_uuid = eval(dic_value["app_label_uuid"])
        except:
            raise error.nonamevalue()
        
        try:
            url = "{{qa_end_point}}/app-labels/" + app_label_uuid[0]
            path = ["app-labels", app_label_uuid[0]]
        except:
            raise error.notfind()
            
        return url,path

    def update_app_labels_new_url_get(self, dic_value):
        ## for PUT, DELETE app-labels
        ## add uuid to url
        ##
        ## Required parameters
        ##      collection_content
        ##      app_label_uuid
        ##
        try:
            dic_value["collection_content"] in locals().keys()
            dic_value["new_param"] in locals().keys()
            tuple_new_param = eval(dic_value["new_param"])
        except:
            raise error.nonamevalue()
        
        try:
            json_content = json.loads(dic_value["collection_content"])
            json_content["item"][1]["request"]["url"]["raw"] = tuple_new_param[0]
            json_content["item"][1]["request"]["url"]["path"] = tuple_new_param[1]
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()    
        return json_file
            


















