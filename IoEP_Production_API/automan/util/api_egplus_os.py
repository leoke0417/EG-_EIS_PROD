# -*- coding: utf-8 -*-
'''
Created on 2020/07/14

@author: Dustin Lin
'''

import requests, json
import automan.tool.error as error
import boto3
import botocore
from botocore import UNSIGNED
# from warrant.aws_srp import AWSSRP
from warrant_lite import WarrantLite as AWSSRP
import time
import subprocess
import websocket
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'conf', "api_egplus_os.conf"),encoding="utf-8")

class api_egplus_os(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass
   
    def ndtoken_get(self,value_dict):


        dicParm = dict(value_dict)
        #print(config.get('bitbucket.org', 'User'))
        strAWSRegion = config.get("test", 'strUserPoolID').split('_')[0]
        try:
            client = boto3.client('cognito-idp', region_name=strAWSRegion, config = botocore.client.Config(signature_version = UNSIGNED))
            objAWS = AWSSRP(
                    username =  config.get("test", "strUserName"),
                    password =  config.get("test", "strPassword"),
                    pool_id = config.get("test", "strUserPoolID"),
                    client_id =  config.get("test", "strClientID"),
                    client = client
                )
            dicToken = objAWS.authenticate_user()
            strIDToken = dicToken['AuthenticationResult']['IdToken']
            #print(strIDToken)
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            raise error.equalerror()
        return strIDToken
        
    def ndtoken_post_verify(self,value_dict):
        dicParm = dict(value_dict)
        strNDAPIServer = config.get("test",'strNDAPIServerHead') + '-qa' + config.get("test",'strNDAPIServerTail')  
        strExchange_URL = strNDAPIServer + config.get("test",'strNDAPIServerExchangePath')
        dicHeader = {
                config.get("test",'strHeaderAuthoKey'): config.get("test",'strHeaderAuthoValue'),
                config.get("test",'strHeaderContentTypeKey'): config.get("test",'strHeaderContentTypeValue')
            }
        dicBody = {
                config.get("test",'strAWSTypeKey'): config.get("test",'strAWSTypeValue'),
                config.get("test",'strTokenKey'): dicParm['strIDToken'],
                'appUuid': config.get("test",'appUuid')
            }
        jsonBody = json.dumps(dicBody)
        objResponse = requests.post(strExchange_URL, data = jsonBody, headers = dicHeader)
        print('!!!!!!!!!!!!!!!!!!', objResponse)
        status_code = objResponse.status_code
        #dicResponse = objResponse.json()
        if dicParm['returnCode'] == str(status_code) :
            pass
        else:
            raise error.equalerror()
        
        
        
    #===========================================================================
    # ndtoken_get
    # ndtoken_get
    # ndtoken_get
    # ndtoken_get
    # ndtoken_get
    #===========================================================================