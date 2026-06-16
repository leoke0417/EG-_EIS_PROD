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



class api_cfg_mgmt(object):
    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
       pass
    def idtoken_get(self, value_dict):
        dicParm = dict(value_dict)   
        strAWSRegion = dicParm['strUserPoolID'].split('_')[0]
        try:
            client = boto3.client('cognito-idp', region_name=strAWSRegion, config = botocore.client.Config(signature_version = UNSIGNED))
            objAWS = AWSSRP(
                    username = dicParm['strUserName'], 
                    password = dicParm['strPassword'], 
                    pool_id = dicParm['strUserPoolID'], 
                    client_id = dicParm['strClientID'], 
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
    
    def ndtoken_get(self, value_dict):
        dicParm = dict(value_dict)
        try:
            if dicParm['NDAPIServerState'] == 'production':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + dicParm['strNDAPIServerTail']
            elif dicParm['NDAPIServerState'] == 'staging':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + '-qa' + dicParm['strNDAPIServerTail']    
            strExchange_URL = strNDAPIServer + dicParm['strNDAPIServerExchangePath']  
            #strNDAPIServerPath = /v1/oauth2/tokens/exchange
            #strFinalAutho = '%s %s' % (dicParm['strPrefixOfAutho'], dicParm['strIDToken'])
            #strPrefixOfAutho = 'Bearer', strIdToken is a token got from idtoken_get
            dicHeader = {
                    dicParm['strHeaderAuthoKey']: dicParm['strHeaderAuthoValue'],
                    dicParm['strHeaderContentTypeKey']: dicParm['strHeaderContentTypeValue']
                }
            #strHeaderAuthoKey = 'accept', strHeaderAuthoValue = 'application/json'
            #strHeaderAutho = 'Authorization'
            #strHeaderContentTypeKey = 'Content-Type', strHeaderContentTypeValue = 'application/json'
            
            dicBody = {
                    dicParm['strAWSTypeKey']: dicParm['strAWSTypeValue'],
                    dicParm['strTokenKey']: dicParm['strIDToken'],
                    'appUuid': '123123dfsdf34234'
                }
            
            
            #strAWSTypeKey = 'type', strAWSTypeValue = 'cognito'
            #strTokenKey = 'token', strIdToken same as id token, which got from idtoken_get func.
            if dicParm['strRemoveHeaderValue'] == 'none':
                pass
            else:
                del dicHeader[dicParm['strRemoveHeaderValue']]
            #for missing header info. test
            if dicParm['strRemoveBodyValue'] == 'none':
                pass
            else:
                del dicBody[dicParm['strRemoveBodyValue']]
            #for missing body info. test
            jsonBody = json.dumps(dicBody)
            if dicParm['method'] == 'post':
                #correct
                objResponse = requests.post(strExchange_URL, data = jsonBody, headers = dicHeader)
                pass
            elif dicParm['method'] == 'get':
                objResponse = requests.get(strExchange_URL, data = jsonBody, headers = dicHeader)
                #wrong
                pass
            elif dicParm['method'] == 'put':
                objResponse = requests.put(strExchange_URL, data = jsonBody, headers = dicHeader)
                #wrong
                pass
            #print('!!!!!!!!!!!!!!!!!!', objResponse)
            if dicParm['returnCode'] == str(200):
                dicResponse = objResponse.json()
                
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                print(strExchange_URL)
                print(dicHeader)
                print(jsonBody)
                print(objResponse)
                print(dicResponse)
                print(dicResponse['accessToken'])
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                
                if objResponse.status_code != 200:
                    print(objResponse)
                    raise error.equalerror()
                else:
                    #print('access token!!!!!!!!!!!!!!!!!\n',dicResponse['access_token'])
                    return dicResponse['accessToken']
            elif dicParm['returnCode'] == str(401):
                print(objResponse)
                pass
            elif dicParm['returnCode'] == str(403):
                print(objResponse)
                pass
            elif dicParm['returnCode'] == str(414):
                print(objResponse)
                pass
            elif dicParm['returnCode'] == str(500):
                print(objResponse)
                pass
            else:
                raise error.equalerror()            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            if dicParm['except'] == 'ignore':
                #有些test case跑進except是正常的但因進入except結果會為fail，當#except#=ignore時直接跳過except，強制讓結果為pass
                pass
            else:
                raise error.equalerror()
                
        
    
    def gwm_associate_get(self, value_dict):
        matchFlag = False
        dicParm = dict(value_dict)
        try:
            if dicParm['NDAPIServerState'] == 'production':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + dicParm['strNDAPIServerTail']
            elif dicParm['NDAPIServerState'] == 'staging':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + '-qa' + dicParm['strNDAPIServerTail']  
            strGWM_URL = strNDAPIServer + dicParm['strNDAPIServerPath_GwAs'] 
            #strNDAPIServerPath = ​/v1​/associations/gateways
            strGWM_Autho = '%s %s' % (dicParm['strAuthoType_GwAs'], dicParm['strNDToken'])
            #strAuthoType = Bearer
            #NDToken is got from ndtoken_get function
            dicGWMHeader = {
                    dicParm['strHeaderAuthoKey_GwAs']: dicParm['strHeaderAuthoValue_GwAs'],
                    dicParm['strHeaderAutho_GwAs']: strGWM_Autho,
                    dicParm['strHeaderContentTypeKey_GwAs']: dicParm['strHeaderContentTypeValue_GwAs']
                }
            #strHeaderAuthoKey = 'accept', strHeaderAuthoValue = 'application/json'
            #strHeaderAutho = 'Authorization'
            #strHeaderContentTypeKey = 'Content-Type', strHeaderContentTypeValue = 'application/json'
            dicGWMBody = {dicParm['strPIDKey_GwAs']: dicParm['strGWM_UUID_GwAs']}
            
            #strPIDKey = 'profileId'
            #strGWM_UUID is the gateway id which for testing
            if dicParm['strRemoveHeaderValue_GwAs'] == 'none':
                pass
            else:
                del dicGWMHeader[dicParm['strRemoveHeaderValue_GwAs']]
            #for missing header info. test
            if dicParm['strRemoveBodyValue_GwAs'] == 'none':
                pass
            else:
                del dicGWMBody[dicParm['strRemoveBodyValue_GwAs']]
            #for missing body info. test
            #print("$$$$$$$$$$$$$$$$$$$$$$$$")
            #print(strGWM_URL)
            #print(dicGWMHeader)
            #print(dicGWMBody)
            jsonGWMBody = json.dumps(dicGWMBody)
            if dicParm['method'] == 'post':
                #correct
                objGWMResponse = requests.post(strGWM_URL, data = jsonGWMBody, headers = dicGWMHeader)
                pass
            elif dicParm['method'] == 'get':
                objGWMResponse = requests.get(strGWM_URL, data = jsonGWMBody, headers = dicGWMHeader)
                #wrong
                pass
            elif dicParm['method'] == 'put':
                objGWMResponse = requests.put(strGWM_URL, data = jsonGWMBody, headers = dicGWMHeader)
                #wrong
                pass

            print('!!!!!!!!!!!!!!!!!!!', objGWMResponse)
            if dicParm['returnCode'] == str(200):
                dicGWMResponse = objGWMResponse.json()
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                print(strGWM_URL)
                print(dicGWMHeader)
                print(jsonGWMBody)
                print(objGWMResponse)
                print(dicGWMResponse)
                print(dicGWMResponse['uuid'])
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                #return dicGWMResponse['uuid']
                if objGWMResponse.status_code == 200: 
                    time.sleep(30)
                    for count in range(0,10):
                        print("try", count)
                        objCmd = subprocess.Popen('adb shell', shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
                        objCmd.stdin.write('cat /data/cfg_mgmt/config.json\n'.encode('utf-8'))
                        objCmd.stdin.write('reboot\n'.encode('utf-8'))
                        objCmd.stdin.write('exit\n'.encode('utf-8'))
                        strConfigFile, err = objCmd.communicate()
                        strConfigFile = strConfigFile.decode('utf-8')
                        dicConfigFile = eval(strConfigFile)
                        if dicConfigFile['gateway']['gateway_uuid'] == dicGWMResponse['uuid']:
                            matchFlag = True
                            print('config.json and cloud match: config.json(gateway_uuid) = ', dicConfigFile['gateway']['gateway_uuid'])
                            break
                        else:
                            pass
                        print('Config.json: ', dicConfigFile)
                        time.sleep(60)
                elif objGWMResponse.status_code != 200:
                    print(objGWMResponse)
                    raise error.equalerror()
                
                if matchFlag == True:
                    pass
                elif matchFlag == False:         
                    raise error.equalerror()
                return dicGWMResponse['uuid']  
                                 
                    
                    
            elif dicParm['returnCode'] == str(400):
                print(objGWMResponse, ": Invalid parameter")
            elif dicParm['returnCode'] == str(401):
                print(objGWMResponse, ": Unauthorized")
            elif dicParm['returnCode'] == str(403):
                print(objGWMResponse)
            elif dicParm['returnCode'] == str(404):
                print(objGWMResponse, ": The gateway doesn't exist")
            elif dicParm['returnCode'] == str(414):
                print(objGWMResponse, ": Request URI too long")
            else:
                raise error.equalerror()
            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            if dicParm['except'] == 'ignore':
                #有些test case跑進except是正常的但因進入except結果會為fail，當#except#=ignore時直接跳過except，強制讓結果為pass
                pass
            else:
                raise error.equalerror() 
        

    def gwm_dissociate_get(self, value_dict):
        matchFlag = False
        dicParm = dict(value_dict)
        try:
            if dicParm['NDAPIServerState'] == 'production':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + dicParm['strNDAPIServerTail']
            elif dicParm['NDAPIServerState'] == 'staging':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + '-qa' + dicParm['strNDAPIServerTail']  
            strGWM_URL = strNDAPIServer + dicParm['strNDAPIServerPath_GwDs'] % dicParm['strGWM_UUID']
            #strNDAPIServerPath = /v1/associations/gateways/%s
            #strGWM_UUID is the gateway id which for testing
            strGWM_Autho = '%s %s' % (dicParm['strAuthoType_GwDs'], dicParm['strNDToken'])
            #strAuthoType = Bearer
            #NDToken is got from ndtoken_get function
            dicGWMHeader = {
                    dicParm['strHeaderAuthoKey_GwDs']: dicParm['strHeaderAuthoValue_GwDs'],
                    dicParm['strHeaderAutho_GwDs']: strGWM_Autho
                }
            #strHeaderAuthoKey = 'accept', strHeaderAuthoValue = '*/*'
            #strHeaderAutho = 'Authorization'
            if dicParm['strRemoveHeaderValue_GwDs'] == 'none':
                pass
            else:
                del dicGWMHeader[dicParm['strRemoveHeaderValue_GwDs']]
            #for missing header info. test
            #print('$$$$$$$$$$$$$$$$$$$$')
            #print(strGWM_URL)
            #print(dicGWMHeader)
            
            objGWMResponse = requests.delete(strGWM_URL, headers = dicGWMHeader)
            if dicParm['returnCode'] == str(200):
                dicGWMResponse = objGWMResponse.json()
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                print(dicGWMHeader)
                print(objGWMResponse)
                print(dicGWMResponse)
                print('$$$$$$$$$$$$$$$$$$$$$$$')
                if objGWMResponse.status_code == 200:
                    pass
                    #===========================================================
                    # time.sleep(30)
                    # for count in range(0, 10):
                    #     print('try', count)
                    #     objCmd = subprocess.Popen('adb shell', shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
                    #     objCmd.stdin.write('cat /data/cfg_mgmt/config.json\n'.encode('utf-8'))
                    #     objCmd.stdin.write('reboot\n'.encode('utf-8'))
                    #     objCmd.stdin.write('exit\n'.encode('utf-8'))
                    #     strConfigFile, err = objCmd.communicate()
                    #     strConfigFile = strConfigFile.decode('utf-8')
                    #     dicConfigFile = eval(strConfigFile)
                    #     if dicConfigFile['gateway']['gateway_uuid'] == '':
                    #         matchFlag = True
                    #         print('config.json and cloud match: config.json(gateway_uuid) = ', dicConfigFile['gateway']['gateway_uuid'])
                    #         break
                    #     else:
                    #         pass
                    #     print('Config.json: ', dicConfigFile)
                    #     time.sleep(60)
                    #===========================================================
                if objGWMResponse.status_code != 200:
                    print(objGWMResponse)
                    raise error.equalerror()
                
                
                
                if matchFlag == True:
                    pass
                elif matchFlag == False:         
                    raise error.equalerror()
                
                
                
                
            elif dicParm['returnCode'] == str(401):
                print(objGWMResponse, ": Unauthorized")
            elif dicParm['returnCode'] == str(403):
                print(objGWMResponse)
            elif dicParm['returnCode'] == str(414):
                print(objGWMResponse, ": Request URI too long")
            else:
                raise error.equalerror()
                
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            if dicParm['except'] == 'ignore':
                #有些test case跑進except是正常的但因進入except結果會為fail，當#except#=ignore時直接跳過except，強制讓結果為pass
                pass
            else:
                raise error.equalerror() 

    def dev_associate_get(self, value_dict):
        dicParm = dict(value_dict)
        try:
            if dicParm['NDAPIServerState'] == 'production':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + dicParm['strNDAPIServerTail']
            elif dicParm['NDAPIServerState'] == 'staging':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + '-qa' + dicParm['strNDAPIServerTail']  
            strDEV_URL = strNDAPIServer + dicParm['strNDAPIServerPath_DevAs']
            #strNDAPIServerPath = /v1/associations/devices
            strDEV_Autho = '%s %s' % (dicParm['strAuthoType_DevAs'], dicParm['strNDToken'])
            #strAuthoType = Bearer
            #NDToken is got from ndtoken_get func.
            dicDEVHeader = {
                    dicParm['strHeaderAuthoKey_DevAs']: dicParm['strHeaderAuthoValue_DevAs'],
                    dicParm['strHeaderAutho_DevAs']: strDEV_Autho,
                    dicParm['strHeaderContentTypeKey_DevAs']: dicParm['strHeaderContentTypeValue_DevAs']
                }
            #strHeaderAuthoKey = 'accept', strHeaderAuthoValue = 'application/json'
            #strHeaderAutho = 'Authorization'
            #strHeaderContentTypeKey = 'Content-Type', strHeaderContentTypeValue = 'application/json'
            dicDEVBody = {
                    dicParm['strNameKey_DevAs']: dicParm['strNameValue_DevAs'],
                    dicParm['strModelKey_DevAs']: dicParm['strModelValue_DevAs'],
                    dicParm['strGWMUUIDKey_DevAs']: dicParm['strGWMUUIDValue_DevAs'],
                    dicParm['strServiceKey_DevAs']: dicParm['strServiceValue_DevAs'],
                    dicParm['strAttributesKey_DevAs']: {
                            dicParm['strMACKey_DevAs']: dicParm['strMACValue_DevAs']
                        } 
                }
            #strNameKey = name, strNameValue = device's name
            #strModelKey = model, strModelValue = model type
            #strGWMUUIDKey = gateway_uuid, strGWMUUIDValue = the gw which connect to the deivce
            #strServiceKey = service, strServiceValue = ble (the way to connect device and gateway)
            #strAttributesKey = attributes
            #strMACKey = mac_address, strMACValue = device's MAC address
            if dicParm['strRemoveHeaderValue_DevAs'] == 'none':
                pass
            else:
                del dicDEVHeader[dicParm['strRemoveHeaderValue_DevAs']]
            #for missing header info. test
            if dicParm['strRemoveBodyValue_DevAs'] == 'none':
                pass
            elif dicParm['strRemoveBodyValue_DevAs'] == 'macAddress':
                del dicDEVBody['attributes']['macAddress']
            else:
                del dicDEVBody[dicParm['strRemoveBodyValue_DevAs']]
            #for missing body info. test
            jsonDEVBody = json.dumps(dicDEVBody)
            #print('@@@@@@@@@@@@@@@@@@@@@@@')
            #print(strDEV_URL)
            #print(jsonDEVBody)
            #print(dicDEVHeader)
            
            if dicParm['method'] == 'post':
                #correct
                objDEVResponse = requests.post(strDEV_URL, data = jsonDEVBody, headers = dicDEVHeader)
                pass
            elif dicParm['method'] == 'get':
                objDEVResponse = requests.get(strDEV_URL, data = jsonDEVBody, headers = dicDEVHeader)
                pass
            elif dicParm['method'] == 'put':
                objDEVResponse = requests.put(strDEV_URL, data = jsonDEVBody, headers = dicDEVHeader)
                pass
          
            print(objDEVResponse)
            if dicParm['returnCode'] == str(200):
                dicDEVResponse = objDEVResponse.json()
                #print('$$$$$$$$$$$$$$$$$$$$$$$')
                #print(dicDEVResponse)
                #print(dicDEVResponse['uuid'])
                #print('$$$$$$$$$$$$$$$$$$$$$$$')
                return dicDEVResponse['uuid']
                if objDEVResponse.status_code != 200:
                    print(objDEVResponse)
                    raise error.equalerror()
            elif dicParm['returnCode'] == str(400):
                print(objDEVResponse, ": Invalid parameter")
            elif dicParm['returnCode'] == str(401):
                print(objDEVResponse, ": Unauthorized")
            elif dicParm['returnCode'] == str(403):
                print(objDEVResponse)
            elif dicParm['returnCode'] == str(404):
                print(objDEVResponse, ": The gateway doesn't exist")
            elif dicParm['returnCode'] == str(414):
                print(objDEVResponse, ": Requset URI too long")
            else:
                raise error.equalerror()
                

        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            if dicParm['except'] == 'ignore':
                #有些test case跑進except是正常的但因進入except結果會為fail，當#except#=ignore時直接跳過except，強制讓結果為pass
                pass
            else:
                raise error.equalerror() 
            

    def dev_dissociate_get(self, value_dict):
        dicParm = dict(value_dict)
        try:
            
            if dicParm['NDAPIServerState'] == 'production':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + dicParm['strNDAPIServerTail']
            elif dicParm['NDAPIServerState'] == 'staging':
                strNDAPIServer = dicParm['strNDAPIServerHead'] + '-qa' + dicParm['strNDAPIServerTail']  
            strDEV_URL = strNDAPIServer + dicParm['strNDAPIServerPath_DevDs'] % dicParm['strDEV_UUID']
            #strNDAPIServer = https://api-eg3.nextdrive.io or add -stg, -dev behind eg3
            #strNDAPIServerPath = /v1/associations/devices/%s
            #strDEV_UUID is the device id which for testing
            strDEV_Autho = '%s %s' % (dicParm['strAuthoType_DevDs'], dicParm['strNDToken'])
            #strAuthoType = Bearer
            #NDToken is got form ndtoken_get func.
            dicDEVHeader = {
                    dicParm['strHeaderAuthoKey_DevDs']: dicParm['strHeaderAuthoValue_DevDs'],
                    dicParm['strHeaderAutho_DevDs']: strDEV_Autho
                }
            #strHeaderAuthoKey = 'accept', strHeaderAuthoValue = '*/*'
            #strHeaderAutho = 'Authorization'
            if dicParm['strRemoveHeaderValue_DevDs'] == 'none':
                pass
            else:
                del dicDEVHeader[dicParm['strRemoveHeaderValue_DevDs']]
            #for missing header info. test
            #print('####################')
            #print(strDEV_URL)
            #print(dicDEVHeader)
            objDEVResponse = requests.delete(strDEV_URL, headers = dicDEVHeader)
            if dicParm['returnCode'] == str(200):
                dicDEVResponse = objDEVResponse.json()
                #print('$$$$$$$$$$$$$$$$$$$$$$$')
                #print(dicParm['strDEV_UUID'])
                #print(objDEVResponse)
                #print(dicDEVResponse)
                #print('$$$$$$$$$$$$$$$$$$$$$$$')
                if objDEVResponse.status_code != 200:
                    print(objDEVResponse)
                    raise error.equalerror()
            elif dicParm['returnCode'] == str(401):
                print(objDEVResponse, ": Unauthorized")
            elif dicParm['returnCode'] == str(403):
                print(objDEVResponse)
            elif dicParm['returnCode'] == str(414):
                print(objDEVResponse, ": Requset URI too long")
            else:
                raise error.equalerror()
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            if dicParm['except'] == 'ignore':
                #有些test case跑進except是正常的但因進入except結果會為fail，當#except#=ignore時直接跳過except，強制讓結果為pass
                pass
            else:
                raise error.equalerror() 

        