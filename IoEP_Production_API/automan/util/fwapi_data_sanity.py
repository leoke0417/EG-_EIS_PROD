# -*- coding: utf-8 -*-
'''
Created on 2020/07/14

@author: Dustin Lin
'''
from automan.tool.verify import Verify
from automan.util.nddb import nddb
import requests, json
import automan.tool.error as error
import boto3
import botocore
from botocore import UNSIGNED
from warrant.aws_srp import AWSSRP
import time,datetime
import subprocess
#import websocket



class fwapi_data_sanity(object):
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
            print(strIDToken)
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            raise error.equalerror() 
        return strIDToken
    
    def ioeapi_device_data_get(self, value_dict):
        dicParm = dict(value_dict)
        try:
            if dicParm['env'] == 'production':
                strNDAPIServer = 'https://ioeapi.nextdrive.io'
                dicHeader = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-ND-TOKEN':'fLMNO0XGJuDadVnpYDM8p3i/FUYJXG8Ur/FQX/1'
                }
            elif dicParm['env'] == 'qa':
                strNDAPIServer = 'https://ioeapi-qa.nextdrive.io'
                dicHeader = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-ND-TOKEN':'pKZ5x7EzcJ+Kv2DgATig9TsyWvkn+50NInPMmBo'
                }     
            strIoEAPI_data_URL = strNDAPIServer + dicParm['strDeviceDataPath']  
            
            #production service Device Data monitor x-nd-token 'fLMNO0XGJuDadVnpYDM8p3i/FUYJXG8Ur/FQX/1'

            
            #get epoch time of two hours before
            #print(str(time.time()-7200))
            time_start = round((time.time()-7200)*1000)
            time_now = round(time.time()*1000)
            #print(str(time_start))
            dicBody = {
                    
                    "queries": [
                       {
                         "deviceUuid": dicParm['dev_uuid'],
                         "scopes": [
                              dicParm['data_scope']
                           ]
                       }
                    ],
                    "time": {
                        "startTime": time_start,
                        "endTime": time_now
                    },
                    "maxCount": 100,
                    "offset": 0
            }
            
            
            
            print(dicBody)
            jsonBody = json.dumps(dicBody)
            #POST only
            objResponse = requests.post(strIoEAPI_data_URL, data = jsonBody, headers = dicHeader)
           
            #print('!!!!!!!!!!!!!!!!!!', objResponse)
            ##if dicParm['returnCode'] == str(200):
            dicResponse = objResponse.json()
            print(dicResponse['totalCount'])
            data_count = str(dicResponse['totalCount'])
            return data_count
           
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
                            
    def ioeapi_device_data2_get(self, value_dict):
        dicParm = dict(value_dict)
        try:
            if dicParm['env'] == 'production':
                strNDAPIServer = 'https://ioeapi.nextdrive.io'
                dicHeader = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-ND-TOKEN':'fLMNO0XGJuDadVnpYDM8p3i/FUYJXG8Ur/FQX/1'
                }
            elif dicParm['env'] == 'qa':
                strNDAPIServer = 'https://ioeapi-qa.nextdrive.io'
                dicHeader = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-ND-TOKEN':'pKZ5x7EzcJ+Kv2DgATig9TsyWvkn+50NInPMmBo'
                }     
            strIoEAPI_data_URL = strNDAPIServer + dicParm['strDeviceDataPath']  
            
            #production service Device Data monitor x-nd-token 'fLMNO0XGJuDadVnpYDM8p3i/FUYJXG8Ur/FQX/1'
            

            #unit=3600*24
            #time_now=int(time.time())
            #time_now = round(time.time()*1000)
            #print(str(time_start))
            time_today=(round(datetime.datetime.now().replace(hour=8,minute=0,second=0,microsecond=0).timestamp()))*1000
            time_period=int(dicParm['time_period'])
            time_start = time_today-time_period*1000
            
            dicBody = {
                    
                    "queries": [
                       {
                         "deviceUuid": dicParm['dev_uuid'],
                         "scopes": [
                              dicParm['data_scope']
                           ]
                       }
                    ],
                    "time": {
                        "startTime": time_start,
                        "endTime": time_today
                    },
                    "maxCount": 100,
                    "offset": 0
            }
            
            
            
            print(dicBody)
            jsonBody = json.dumps(dicBody)
            #POST only
            objResponse = requests.post(strIoEAPI_data_URL, data = jsonBody, headers = dicHeader)
           
            #print('!!!!!!!!!!!!!!!!!!', objResponse)
            ##if dicParm['returnCode'] == str(200):
            dicResponse = objResponse.json()
            print(dicResponse['totalCount'])
            data_count = str(dicResponse['totalCount'])
            return data_count
           
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
        
    
    def db_connection_get(self, value_dict):
        
        dicParm = dict(value_dict)
        try:
            
            dicParm['strDB'] = 'eg3'
            dicParm['strHost'] = 'pgbouncer-qa.nextdrive.io'
            dicParm['strPort'] = '15432' 
            dicParm['strUser'] = 'qa_user'
            #dicParm['strPW'] in locals().keys()
            
            #nddb connection setup
            dicParm['strPW']='kGm:A.=#=])6P^6j'
            data_db=nddb(dicParm)
           
            data_db.closeDB()
            

            print('!!!!!!closed!!!!!!!!!!!!!')
            
            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)

    def device_data_count_get(self, value_dict):
        
        dicParm = dict(value_dict)
        dbParm = {}
        try:
            
            dbParm['strDB'] = 'eg3'
            dbParm['strHost'] = 'pgbouncer-qa.nextdrive.io'
            dbParm['strPort'] = '15432' 
            dbParm['strUser'] = 'qa_user'
            dbParm['strPW'] ='kGm:A.=#=])6P^6j'
            dicParm['dev_uuid'] in locals().keys()
            dicParm['data_uuid'] in locals().keys()
            #dicParm['strPW'] in locals().keys()
            
            #two hours before current time as target time
            target_time = datetime.datetime.utcfromtimestamp(time.time()-7200).strftime('%Y-%m-%d %H:%M:%S')


            #nddb connection setup
            
            data_db=nddb(dbParm)
            sql_query="select count(value) from eg3.public.device_data where " + \
                      "device_uuid = '" + dicParm['dev_uuid'] + "' " + \
                      "and data_uuid = '" + dicParm['data_uuid'] + "' " + \
                      "and generated_time > '" + target_time + "' "

            row_count = data_db.query(sql_query)
            print(str(row_count[0][0]))
           
            data_db.closeDB()
            return str(row_count[0][0])

            
            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
    
    def device_data_rows_get(self, value_dict):
        
        dicParm = dict(value_dict)
        dbParm = {}
        try:
            
            dbParm['strDB'] = 'eg3'
            dbParm['strHost'] = 'pgbouncer-qa.nextdrive.io'
            dbParm['strPort'] = '15432' 
            dbParm['strUser'] = 'qa_user'
            dbParm['strPW'] ='kGm:A.=#=])6P^6j'
            dicParm['dev_uuid'] in locals().keys()
            dicParm['data_uuid'] in locals().keys()
            #two hours before current time as target time
            target_time = datetime.datetime.utcfromtimestamp(time.time()-7200).strftime('%Y-%m-%d %H:%M:%S')
            #target_time = (time.localtime -7200).format('YYYY-MM-HH hh:mm:ss') 
            #dicParm['target_time'] in locals().keys()
            #dicParm['dev_uuid'] in locals().keys()
            #nddb connection setup
            print(str(target_time))
            data_db=nddb(dbParm)

            sql_query="select value , generated_time from eg3.public.device_data where " + \
                      "device_uuid = '" + dicParm['dev_uuid'] + "' " + \
                      "and data_uuid = '" + dicParm['data_uuid'] + "' " + \
                      "and generated_time > '" + target_time + "' order by generated_time desc"

            data_row = data_db.query(sql_query)
            print(data_row)
            data_db.closeDB()
            
            return data_row
            
            
            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
    
    def dev_data_count_verify(self, value_dict):
        ##  Required parameters:
        ##      data        - Source content
        ##      key           - Expected result
        ##      criteria        - Check condition
        try:
            ##value_dict['data'] in locals().keys()
            value_dict['key'] in locals().keys()
            value_dict['value'] in locals().keys()
            value_dict['criteria'] in locals().keys()
            
        except:
            #KeyError
            raise error.nonamevalue()
                
        value_dict['system_value'] = value_dict['key']
        
                
        print("Value: " + value_dict['value'] + ", System_value: " + value_dict['system_value'])
        if Verify().verify(value_dict):
            pass
    
    
    def on_message(self, ws, message):
        print('on_message')
        print(ws)
        print(message)
        print('----------')
        
    def on_error(self, ws, error):
        print('on_error')
        print(ws)
        print('----------')
        
    def on_close(self, ws):
        print('on_clolse')
        print(ws)
        print('--- closed ---')
        
    def device_list_get(self, value_dict):
        dicParm = dict(value_dict)
        strUrl = 'wws://websocket-stg.nextdrive.io/register'
        dicData = {
                dicParm['strTypeKey']: dicParm['strTypeValue'],
                dicParm['strAppIdKey']: dicParm['strAppIdValue'],
                dicParm['strSessionIdKey']: dicParm['strSessionIdValue'],
                dicParm['strDatakey']: {
                        dicParm['strVersionKey']: dicParm['strVersionValue'],
                        dicParm['strServiceKey']: dicParm['strServiceValye'],
                        dicParm['strGwUuidKey']: dicParm['strGwUuidValue']
                    }
            }
        dicHeader = {
                dicParm['strTypeKey']: dicParm['strTypeValue'],
                dicParm['strCertKey']: dicParm['strCertValye'],
                dicParm['strAppUuidKey']: dicParm['strAppUuidValue']
            }
        
    def gw_config_verify(self, value_dict):
        ##  Required parameters:
        ##      data        - Source content
        ##      key           - Expected result
        ##      criteria        - Check condition
        try:
            ##value_dict['data'] in locals().keys()
            value_dict['key'] in locals().keys()
            value_dict['gw_name'] in locals().keys()
            value_dict['criteria'] in locals().keys()
            
        except:
            #KeyError
            raise error.nonamevalue()
        adb_connect = 'adb -s '+ value_dict['gw_name'] +' shell'
        #print('try', count)
        objCmd = subprocess.Popen(adb_connect, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        objCmd.stdin.write('cat /data/cfg_mgmt/config.json\n'.encode('utf-8'))
        objCmd.stdin.write('exit\n'.encode('utf-8'))
        strConfigFile, err = objCmd.communicate()
        strConfigFile = strConfigFile.decode('utf-8')
        dicConfigFile = eval(strConfigFile)
            ##if dicConfigFile['gateway']['gateway_uuid'] == '':
            ##    matchFlag = True
            ##    print('config.json and cloud match: config.json(gateway_uuid) = ', dicConfigFile['gateway']['gateway_uuid'])
            ##    break
            ##else:
            ##    pass
        print('Config.json: ', dicConfigFile)
        ##time.sleep(10)
        
        value_dict['system_value'] = value_dict['key']
        value_dict['value'] = dicConfigFile['gateway']['gateway_uuid']
                
        print("Value: " + value_dict['value'] + ", System_value: " + value_dict['system_value'])
        if Verify().verify(value_dict):
            pass    
            
    def dev_config_verify(self, value_dict):
        ##  Required parameters:
        ##      data        - Source content
        ##      key           - Expected result
        ##      criteria        - Check condition
        try:
            ##value_dict['data'] in locals().keys()
            value_dict['key'] in locals().keys()
            value_dict['gw_name'] in locals().keys()
            value_dict['criteria'] in locals().keys()
            
        except:
            #KeyError
            raise error.nonamevalue()
        adb_connect = 'adb -s '+ value_dict['gw_name'] +' shell'
        for count in range(0, 10):
            print('try', count)
            objCmd = subprocess.Popen(adb_connect, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
            objCmd.stdin.write('cat /data/cfg_mgmt/config.json\n'.encode('utf-8'))
            objCmd.stdin.write('reboot\n'.encode('utf-8'))
            objCmd.stdin.write('exit\n'.encode('utf-8'))
            strConfigFile, err = objCmd.communicate()
            strConfigFile = strConfigFile.decode('utf-8')
            dicConfigFile = eval(strConfigFile)
            if dicConfigFile['device']['device_uuid'] == '':
                matchFlag = True
                print('config.json and cloud match: config.json(device_uuid) = ', dicConfigFile['device']['device_uuid'])
                break
            else:
                pass
            print('Config.json: ', dicConfigFile)
            time.sleep(60)
        
        value_dict['system_value'] = value_dict['key']
        value_dict['value'] = dicConfigFile['device']['device_uuid']
                
        print("Value: " + value_dict['value'] + ", System_value: " + value_dict['system_value'])
        if Verify().verify(value_dict):
            pass
            
    def db_post_get(self, value_dict):
        
        dicParm = dict(value_dict)
        dbParm = {}
        try:
            
            dbParm['strDB'] = 'eg3'
            dbParm['strHost'] = 'pgbouncer-qa.nextdrive.io'
            dbParm['strPort'] = '15432' 
            dbParm['strUser'] = 'qa_user'
            dbParm['strPW'] ='kGm:A.=#=])6P^6j'
            dicParm['audience_conditions'] in locals().keys()
            dicParm['name'] in locals().keys()

            today = datetime.date.today()
            yesterday=str(today - datetime.timedelta(days=1))
            #nddb connection setup
            
            data_db=nddb(dbParm)
            #detail_content
            sql_query="select title from eg3.public.posts where " + \
                      "audience_conditions = '" 'userId='+ dicParm['audience_conditions'] + "' " + \
                      "and name = '" + dicParm['name'] + "' " + \
                      "and published_at > '"+yesterday+ " 00:00:00.000'"
            #print(sql_query)

            post_title = data_db.query(sql_query)        
            data_db.closeDB()
            return str(post_title[0][0])

            
            
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            
    def post_yesterday_title_verify(self, value_dict):

        try:
            value_dict['value'] in locals().keys()
            
        except:
            raise error.nonamevalue()
                
        today = datetime.date.today()
        yesterday=(str(today - datetime.timedelta(days=1))).replace("-","/",2)
        #print(yesterday)
        
        if yesterday in value_dict['value']:
            print("Post title : " + value_dict['value'] + " exist " + yesterday)
            pass
        else:
            print("Post title : " + value_dict['value'] + " not exist " + yesterday)
            raise error.nonamevalue()

    
    def pixig_result_get(self, valueDict):

        try:
            valueDict['count_battery'] in locals().keys()
           
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 60 min | 24 | " + valueDict['count_battery'] + " | Battery\n" + returnText
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Pixi Motion\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
            
    def thermo_result_get(self, valueDict):

        try:
            valueDict['count_battery'] in locals().keys()
            valueDict['count_temperature'] in locals().keys()
            valueDict['count_humidity'] in locals().keys()
             
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 1 min   | 1440 | " + valueDict['count_battery'] + " | battery\n" + returnText
            returnText = " 1 min   | 1440 | " + valueDict['count_temperature'] + " | temperature\n" + returnText
            returnText = " 1 min   | 1440 | " + valueDict['count_humidity'] + " | humidity\n" + returnText
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Pixi Thermo\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()


    def smartmeter_result_get(self, valueDict):

        try:
            valueDict['count_sm_normalUsage'] in locals().keys()
            valueDict['count_sm_reverseUsage'] in locals().keys()
            valueDict['count_sm_instanceElectricity'] in locals().keys()
            valueDict['count_sm_instanceCurrents'] in locals().keys()
            valueDict['count_sm_instanceCurrentsT'] in locals().keys()            
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 1 min   | 1440 | " + valueDict['count_sm_instanceCurrentsT'] + " | instanceCurrentsT\n" + returnText
            returnText = " 1 min   | 1440 | " + valueDict['count_sm_instanceCurrents'] + " | instanceCurrents\n" + returnText
            returnText = " 30 sec | 2880 | " + valueDict['count_sm_instanceElectricity'] + " | instanceElectricity\n" + returnText
            returnText = " 30 min |     48 |   " + valueDict['count_sm_reverseUsage'] + " | reverseUsage\n" + returnText
            returnText = " 30 min |     48 |   " + valueDict['count_sm_normalUsage'] + " | normalUsage\n" + returnText
            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Smart-meter\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
    def fuelcell_result_get(self, valueDict):

        try:
            valueDict['count_powerGenerationStatus'] in locals().keys()
            valueDict['count_generatedElectricity'] in locals().keys()
            valueDict['count_instanceElectricity'] in locals().keys()
        
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = "   5 min |   288 |   " + valueDict['count_powerGenerationStatus'] + " | powerGenerationStatus\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_generatedElectricity'] + " | generatedElectricity\n" + returnText
            returnText = "   1 min | 1440 | " + valueDict['count_instanceElectricity'] + " | instanceElectricity\n" + returnText

            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Fuel Cell\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
    def pv_result_get(self, valueDict):

        try:
            valueDict['count_pv_generatedElectricity'] in locals().keys()
            valueDict['count_pv_instanceElectricity'] in locals().keys()
        
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = "   5 min |   288 |   " + valueDict['count_pv_generatedElectricity'] + " | generatedElectricity\n" + returnText
            returnText = "   1 min | 1440 | " + valueDict['count_pv_instanceElectricity'] + " | instanceElectricity\n" + returnText

            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: PV\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
    def pdb_result_get(self, valueDict):

        try:
            valueDict['count_pdb_normalUsage'] in locals().keys()
            valueDict['count_pdb_reverseUsage'] in locals().keys()
        
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = "   5 min | 288 | " + valueDict['count_pdb_reverseUsage'] + " | reverseUsage\n" + returnText
            returnText = "   5 min | 288 | " + valueDict['count_pdb_normalUsage'] + " | normalUsage\n" + returnText

            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: PDB\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()

    def battery_result_get(self, valueDict):

        try:
            valueDict['count_battery_storedElectricityPercent'] in locals().keys()
            valueDict['count_battery_chargeableElectricity'] in locals().keys()
            valueDict['count_battery_instantChargingOrDischargingElectricity'] in locals().keys()
            valueDict['count_battery_acChargingEnergy'] in locals().keys()
            valueDict['count_battery_acChargeableElectricEnergy'] in locals().keys()
            valueDict['count_battery_workingOperationStatus'] in locals().keys()
            valueDict['count_battery_acDischargeableElectricEnergy'] in locals().keys()
            valueDict['count_battery_acDischargingEnergy'] in locals().keys()
            valueDict['count_battery_dischargeableElectricity'] in locals().keys()
            valueDict['count_battery_storedElectricityAmpereHour'] in locals().keys()
            
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 15 min |     96 |     " + valueDict['count_battery_chargeableElectricity'] + " | chargeableElectricity\n" + returnText
            returnText = " 15 min |     96 |     " + valueDict['count_battery_dischargeableElectricity'] + " | ischargeableElectricity\n" + returnText
            returnText = " 10 min |   144 |   " + valueDict['count_battery_storedElectricityAmpereHour'] + " | storedElectricityAmpereHour\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_battery_acChargingEnergy'] + " | acChargingEnergy\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_battery_acChargeableElectricEnergy'] + " | acChargeableElectricEnergy\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_battery_acDischargeableElectricEnergy'] + " | acDischargeableElectricEnergy\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_battery_acDischargingEnergy'] + " | acDischargingEnergy\n" + returnText
            returnText = "   5 min |   288 |   " + valueDict['count_battery_storedElectricityPercent'] + " | storedElectricityPercent\n" + returnText
            returnText = "   1 min | 1440 | " + valueDict['count_battery_instantChargingOrDischargingElectricity'] + " | instantChargingOrDischargingElectricity\n" + returnText                     
            returnText = "   1 min | 1440 | " + valueDict['count_battery_workingOperationStatus'] + " | workingOperationStatus\n" + returnText
            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Battery \n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
    def t2ms_result_get(self, valueDict):

        try:
            valueDict['count_t2ms_meterUnit'] in locals().keys()
            valueDict['count_t2ms_normalUsage'] in locals().keys()
            valueDict['count_t2ms_reverseUsage'] in locals().keys()
            valueDict['count_t2ms_currentReverseUsage'] in locals().keys()
            valueDict['count_t2ms_currentNormalUsage'] in locals().keys()

            
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 30 min |     48 |     " + valueDict['count_t2ms_meterUnit'] + " | meterUnit\n" + returnText
            returnText = " 30 min |     48 |     " + valueDict['count_t2ms_normalUsage'] + " | normalUsage\n" + returnText
            returnText = " 30 min |     48 |     " + valueDict['count_t2ms_reverseUsage'] + " | reverseUsage\n" + returnText
            returnText = "   1 min | 1440 | " + valueDict['count_t2ms_currentReverseUsage'] + " | currentReverseUsage\n" + returnText
            returnText = "   1 min | 1440 | " + valueDict['count_t2ms_currentNormalUsage'] + " | currentNormalUsage\n" + returnText

            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: T2MS-TypeM \n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()
            
    def wHeater_result_get(self, valueDict):

        try:
            valueDict['count_wHeater_daytimeHeatingShiftTime1'] in locals().keys()
            valueDict['count_wHeater_timeToStartHeating'] in locals().keys()
            valueDict['count_wHeater_waterHeaterStatus'] in locals().keys()
            valueDict['count_wHeater_operationStatus'] in locals().keys()
            valueDict['count_wHeater_waterTemperature'] in locals().keys()
            valueDict['count_wHeater_autoWaterHeatingMode'] in locals().keys()
            valueDict['count_wHeater_participateInEnergyShift'] in locals().keys()
            valueDict['count_wHeater_numberOfEnergyShift'] in locals().keys()
            
            valueDict['fw_version'] in locals().keys()
            fwVersion=valueDict['fw_version']
            valueDict['env'] in locals().keys()
            testingEnvironment = "QA Staging" if valueDict['env'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['env'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        try:
            returnText = ""
            returnText = " 15 min |   96 |   " + valueDict['count_wHeater_daytimeHeatingShiftTime1'] + " | daytimeHeatingShiftTime1\n" + returnText
            returnText = " 15 min |   96 |   " + valueDict['count_wHeater_timeToStartHeating'] + " | timeToStartHeating\n" + returnText
            returnText = " 15 min |   96 |   " + valueDict['count_wHeater_participateInEnergyShift'] + " | participateInEnergyShift\n" + returnText
            returnText = " 15 min |   96 |   " + valueDict['count_wHeater_numberOfEnergyShift'] + " | numberOfEnergyShift\n" + returnText
            returnText = " 10 min | 144 | " + valueDict['count_wHeater_waterHeaterStatus'] + " | waterHeaterStatus\n" + returnText
            returnText = " 10 min | 144 | " + valueDict['count_wHeater_operationStatus'] + " | operationStatus\n" + returnText
            returnText = " 10 min | 144 | " + valueDict['count_wHeater_waterTemperature'] + " | waterTemperature\n" + returnText
            returnText = " 10 min | 144 | " + valueDict['count_wHeater_autoWaterHeatingMode'] + " | autoWaterHeatingMode\n" + returnText


            
            returnText = "Interval | Idealiy | Actural | Device Data scope\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Device: Water Heater \n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "------------------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ data count check for yesterday were finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()