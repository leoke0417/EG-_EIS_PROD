#coding=utf-8
"""
Created on 2020/12/28
@author     : Roger Wei
Project     : API-Service
Test plan   : 
    2020/11
        a.  Authentication
            i.  Get Access Token    - 2020/12/29
        b.  Gateway Management
            i.  Gateway status      - 2020/12/29
            ii. Device List         - 2020/12/30
        c.  Data Acquirement
            i.  Data Retrieval      - 2020/12/31
    2020/12
        a.  Gateway Management
            i.  Upload Interval     - 2021/01/04
        b.  Device Operation
            i.  Device Control      - 2021/01/04
            ii. Device Data Acquire
        c.  Data Acquirement
            i.  Data Callback 
"""
import automan.tool.error as error  
from automan.tool.verify import Verify
import requests, base64, json, re, random
import configparser
import datetime
import time
import os
from sshtunnel import SSHTunnelForwarder
import psycopg2

class api_service(object):
    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(os.path.join(os.getcwd(), "conf", "API_Service.conf"), encoding = "utf-8")
            self.index = "API_Service"  
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()         
        pass

    def DBconnect_get(self):
        try:
            self.objSshTunnel = SSHTunnelForwarder(
                    ssh_address_or_host = (self.config.get("connectDBParam", "strSshKey"), int(self.config.get("connectDBParam", "strSshHostPort"))), #strSshKey:13.115.81.250 strSshHostPort:20022
                    ssh_pkey = os.path.join(os.getcwd(), self.config.get("connectDBParam", "strFolderName"), self.config.get("connectDBParam", "strFileName")), #foldername: conf, filename: qa.pem
                    ssh_username = self.config.get("connectDBParam", "strSshUserName"),
                    remote_bind_address = (self.config.get("connectDBParam", "strStagingDBPublic"), int(self.config.get("connectDBParam", "strDBHostPort")))
                )
            self.objSshTunnel.start()
            print("=====> Server Connected...")
            self.connectDB = psycopg2.connect(
                database = self.config.get("connectDBParam", "strDBName"),
                user = self.config.get("connectDBParam", "strDBAccount"),
                password = self.config.get("connectDBParam", "strDBPwd"),
                sslmode = self.config.get("connectDBParam", "strSslMode"),
                host = self.config.get("connectDBParam", "strHost"),
                port = self.objSshTunnel.local_bind_port
            )
            self.cursor = self.connectDB.cursor()
            print("=====> Database Connected...")

        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()
    
    def closeDBConnection_get(self):
        self.cursor.close()
        self.connectDB.close()
        self.objSshTunnel.stop()
  
    def configFileParser(self):
        ### Parse config file data to parameter (type: dictionary)
        listConfigKey = []
        listConfigValue = []
        try:
            #print("=====>Config Section: {}".format(self.config.sections()))
            for item in self.config[self.index]:
                listConfigKey.append(item)
                listConfigValue.append(self.config[self.index][item])
            dicParam = {}
            for keyValue in range(len(listConfigKey)):
                dicParam[listConfigKey[keyValue]] = listConfigValue[keyValue]
            return dicParam
        except:
            print("=====> Error readConfigToDict")
        
    def nd_token_get(self, valueDict):
        ##  Get an access token from ND-Cloud for calling APIs.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      environment         - Testing environment, available parameters:
        ##          qa
        ##          development
        ##          production
        ##      client_id           - Client ID
        ##      secret_key          - Secret key
        ##      scope               - OAuth scope, available parameters:
        ##          User Management
        ##          Gateway Management
        ##          Data Acquirement
        ##          Device Management
        ##          NextDrive Data Application
        ##
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        
        requestTimeout = 180

        try:
            oauth_token_url = ""
            oauth_scope = ""
            if dicParam['environment'] == "qa":
                oauth_token_url = dicParam['oauth_token_url_qa']
                oauth_scope = dicParam['api_suffix_qa']
            elif dicParam['environment'] == "production":
                oauth_token_url = dicParam['oauth_token_url_production']
                oauth_scope = dicParam['api_suffix_production']
            elif dicParam['environment'] == "development":
                oauth_token_url = dicParam['oauth_token_url_development']
                oauth_scope = dicParam['api_suffix_development']
            
            if dicParam['scope'] == "User Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_user_management']
            elif dicParam['scope'] == "Gateway Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_gateway_management']
            elif dicParam['scope'] == "Data Acquirement":
                oauth_scope = oauth_scope + dicParam['oauth_scope_data_acquirement']
            elif dicParam['scope'] == "Device Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_device_management']
            elif dicParam['scope'] == "NextDrive Data Application":
                oauth_scope = oauth_scope + dicParam['oauth_scope_data_application']
            
            print("Oauth token URL:", oauth_token_url)
            print("Oauth scope:", oauth_scope)
                        
            ##  Create HTTP request headers
            authValue = '%s:%s' % (dicParam['client_id'], dicParam['secret_key'])
            authValue = authValue.encode('utf-8')
            authValue = base64.b64encode(authValue)
            authValue = '%s %s' % ('Basic', authValue.decode('utf-8'))
            HTTPHeader = { \
                'authorization': authValue, \
                'content-type': 'application/x-www-form-urlencoded' \
                }
        except Exception as e:
            print(e)
            raise error.onqaserror()  
   
        ##  Create HTTP request body
        HTTPBody = { \
            'grant_type': 'client_credentials', \
            'scope': oauth_scope \
            }
        
        ##  Do HTTP request by POST
        try:
            print("Request headers: ", HTTPHeader)
            print("Request body: ", HTTPBody)
            accessToken = requests.post(oauth_token_url, \
                headers = HTTPHeader, \
                data = HTTPBody, \
                timeout = requestTimeout \
                )
            print("HTTP status code: ", accessToken.status_code)
            if accessToken.status_code is not 200:
                raise error.notfind()
            else:
                accessToken = accessToken.json()
                print("HTTP response: ", accessToken)
                return accessToken["access_token"]
        except Exception as e:
            print(e)
            raise error.notfind()
        
    def HTTP_GET_response_get(self, valueDict):
        ##  HTTP request by GET method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters :
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        requestTimeout = 180
        try:
            valueDict['url'] in locals().keys()
            valueDict['header'] in locals().keys()
        except:
            #KeyError
            raise error.nonamevalue()
 
        try:
            HTTPResponse = requests.get(valueDict['url'], headers = json.loads(valueDict['header']), timeout = requestTimeout)
            statusCode = HTTPResponse.status_code
            HTTPResponse = HTTPResponse.json()
            print("HTTP status code: ", statusCode)
            print("HTTP response: ", HTTPResponse)
            HTTPResponse['statusCode'] = statusCode
            return HTTPResponse
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
 
    def HTTP_POST_response_get(self, valueDict):
        ##  HTTP request by POST method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters :
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        requestTimeout = 180
        try:
            valueDict['url'] in locals().keys()
            valueDict['header'] in locals().keys()
            valueDict['body'] in locals().keys()
        except:
            #KeyError
            raise error.nonamevalue()
 
        try:
            HTTPResponse = requests.post(valueDict['url'], headers = json.loads(valueDict['header']), json = json.loads(valueDict['body']), timeout = requestTimeout)
            statusCode = HTTPResponse.status_code
            HTTPResponse = HTTPResponse.json()
            print("HTTP status code: ", statusCode)
            print("HTTP response: ", HTTPResponse)
            HTTPResponse['statusCode'] = statusCode
            return HTTPResponse
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
 
    def HTTP_PUT_response_get(self, valueDict):
        ##  HTTP request by PUT method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        requestTimeout = 180
        try:
            valueDict['url'] in locals().keys()
            valueDict['header'] in locals().keys()
            valueDict['body'] in locals().keys()
        except:
            #KeyError
            raise error.nonamevalue()
 
        try:
            HTTPResponse = requests.put(valueDict['url'], headers = json.loads(valueDict['header']), json = json.loads(valueDict['body']), timeout = requestTimeout)
            statusCode = HTTPResponse.status_code
            HTTPResponse = HTTPResponse.json()
            print("HTTP status code: ", statusCode)
            print("HTTP response: ", HTTPResponse)
            HTTPResponse['statusCode'] = statusCode
            return HTTPResponse
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
 
    def status_code_verify(self, valueDict):
        ##  Check status code of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response, including 'statusCode'.
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueDict['value'] = str(data['statusCode'])
            print("Actual result: ", valueDict['value'], "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
 
    def gateway_status_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Gateway Management - Gateway Status
        ##
        ##  Required parameters:
        ##      gateway_pid     - Gateway ID
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint    - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/gateways/" + dicParam['gateway_pid'] + "/status"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
   
    def gateway_status_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Gateway Management - Gateway Status
        ##
        ##  Required parameters:
        ##      token           - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = valueDict['token']
            header = "{\"accept\": \"application/json\", \"X-ND-TOKEN\": \"" + authValue + "\"}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
        
    def gateway_status_name_verify(self, valueDict):
        ##  Check gateway name of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            valueDict['value'] = eval(valueDict['value'])
            valueDict['value'] = valueDict['value']['name']
            print("Actual result: " + valueDict['value'] + "\nExpected result: " + valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def gateway_status_model_verify(self, valueDict):
        ##  Check gateway model of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            valueDict['value'] = eval(valueDict['value'])
            valueDict['value'] = valueDict['value']['model']
            print("Actual result: " + valueDict['value'] + "\nExpected result: " + valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def gateway_status_fwVersion_verify(self, valueDict):
        ##  Check gateway firmware version of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            valueDict['value'] = eval(valueDict['value'])
            valueDict['value'] = valueDict['value']['fwVersion']
            print("Actual result: " + valueDict['value'] + "\nExpected result: " + valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
            
    def gateway_status_onlineStatus_verify(self, valueDict):
        ##  Check gateway online status of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            valueDict['value'] = eval(valueDict['value'])
            valueDict['value'] = valueDict['value']['onlineStatus']
            print("Actual result: " + valueDict['value'] + "\nExpected result: " + valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def device_list_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Gateway Management - Device List
        ##
        ##  Required parameters:
        ##      gateway_pid     - Gateway ID
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint    - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/gateways/" + dicParam['gateway_pid'] + "/devices"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
   
    def device_list_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Gateway Management - Device List
        ##
        ##  Required parameters:
        ##      token           - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = valueDict['token']
            header = "{\"accept\": \"application/json\", \"X-ND-TOKEN\": \"" + authValue + "\"}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
        
    def device_list_deviceUuid_verify(self, valueDict):
        ##  Check device list uuid of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            resultList = []
            for item in data['devices']:
                resultList.append(item['deviceUuid'])
                if item['deviceUuid'] in system_value:
                    system_value.remove(item['deviceUuid'])
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = len(system_value)
            valueDict['system_value'] = 0
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def device_list_name_verify(self, valueDict):
        ##  Check device list name of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            resultList = []
            for item in data['devices']:
                resultList.append(item['name'])
                if item['name'] in system_value:
                    system_value.remove(item['name'])
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = len(system_value)
            valueDict['system_value'] = 0
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def device_list_model_verify(self, valueDict):
        ##  Check device list model of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            resultList = []
            for item in data['devices']:
                resultList.append(item['model'])
                if item['model'] in system_value:
                    system_value.remove(item['model'])
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = len(system_value)
            valueDict['system_value'] = 0
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def device_list_onlineStatus_verify(self, valueDict):
        ##  Check device list onlineStatus of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            resultList = []
            for item in data['devices']:
                resultList.append(item['onlineStatus'])
                if item['onlineStatus'] in system_value:
                    system_value.remove(item['onlineStatus'])
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = len(system_value)
            valueDict['system_value'] = 0
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def data_retrieval_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Data Acquirement - Data Retrieval
        ##
        ##  Required parameters:
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint    - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/device-data/query"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
   
    def data_retrieval_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Data Acquirement - Data Retrieval
        ##
        ##  Required parameters:
        ##      token           - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = valueDict['token']
            header = "{\"accept\": \"application/json\"," + \
                "\"X-ND-TOKEN\": \"" + authValue + "\"," + \
                "\"content-type\": \"application/json\"" + \
                "}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
        
    def data_retrieval_ac_body_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Data Acquirement    - Data Retrieval - Air conditioner
        ##
        ##  Required parameters:
        ##      uuid                - Device UUID
        ##
        ##  Request body:
        ##  {
        ##      "queries": [
        ##          {
        ##              "deviceUuid": "{device UUID}",
        ##              "scopes": [
        ##                  "operationStatus"
        ##                  "powerSavingOperation",
        ##                  "operationMode",
        ##                  "temperatureSetting",
        ##                  "airFlow"
        ##              ]
        ##          }
        ##      ],
        ##      "time": {
        ##          "startTime": {Timestamp 15 minutes ago},
        ##          "endTime": {Current timestamp}
        ##      },
        ##      "maxCount": 60,
        ##      "offset": 0
        ##  }
        ##
        try:
            body = "{" + \
                "\"queries\": [" + \
                "{" + \
                "\"deviceUuid\": \"" + valueDict['uuid'] + "\"," + \
                "\"scopes\": [" + \
                "\"operationStatus\"," + \
                "\"powerSavingOperation\"," + \
                "\"operationMode\"," + \
                "\"temperatureSetting\"," + \
                "\"airFlow\"" + \
                "]" + \
                "}" + \
                "]," + \
                "\"time\": {" + \
                "\"startTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time() - 900)) + "," + \
                "\"endTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time())) + "" + \
                "}," + \
                "\"maxCount\": 60," + \
                "\"offset\": 0" + \
                "}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
        
    def data_retrieval_pid_verify(self, valueDict):
        ##  Check data retrieval PID of HTTP response.
        ##  All PID must match gateway PID.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            result = False
            resultList = []
            for item in data['results']:
                resultList.append(item['pid'])
                if item['pid'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def data_retrieval_uuid_verify(self, valueDict):
        ##  Check data retrieval UUID of HTTP response.
        ##  All UUID must match device PID.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            result = False
            resultList = []
            for item in data['results']:
                resultList.append(item['deviceUuid'])
                if item['deviceUuid'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def data_retrieval_model_verify(self, valueDict):
        ##  Check data retrieval model of HTTP response.
        ##  All model must match device model.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            result = False
            resultList = []
            for item in data['results']:
                resultList.append(item['model'])
                if item['model'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def data_retrieval_scope_verify(self, valueDict):
        ##  Check device list scope of HTTP response.
        ##  "system_value" must all be found from scope list.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            resultList = []
            for item in data['results']:
                resultList.append(item['scope'])
                if len(system_value) == 0:
                    break
                if item['scope'] in system_value:
                    system_value.remove(item['scope'])
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = len(system_value)
            valueDict['system_value'] = 0
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
        
    def data_retrieval_generatedTime_verify(self, valueDict):
        ##  Check data retrieval generatedTime of HTTP response.
        ##  All generated time must be range from 0 to current timestamp.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            result = False
            resultList = []
            valueDict['system_value'] = (lambda x: (x.split("."))[0] + "000")(str(time.time()))
            for item in data['results']:
                resultList.append(item['generatedTime'])
                if int(item['generatedTime']) > 0 and int(item['generatedTime']) < int(valueDict['system_value']):
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: 0~", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_uploadedTime_verify(self, valueDict):
        ##  Check data retrieval uploadedTime of HTTP response.
        ##  All generated time must be range from 0 to current timestamp.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            result = False
            resultList = []
            valueDict['system_value'] = (lambda x: (x.split("."))[0] + "000")(str(time.time()))
            for item in data['results']:
                resultList.append(item['uploadedTime'])
                if int(item['uploadedTime']) > 0 and int(item['uploadedTime']) < int(valueDict['system_value']):
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: 0~", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_ac_operationStatus_verify(self, valueDict):
        ##  Check data retrieval air conditioner - operationStatus of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "operationStatus":
                    valueList.append(data['results'][i])
            print("Scope - \"operationStatus\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_ac_powerSavingOperation_verify(self, valueDict):
        ##  Check data retrieval air conditioner - powerSavingOperation of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "powerSavingOperation":
                    valueList.append(data['results'][i])
            print("Scope - \"powerSavingOperation\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_ac_operationMode_verify(self, valueDict):
        ##  Check data retrieval air conditioner - operationMode of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "operationMode":
                    valueList.append(data['results'][i])
            print("Scope - \"operationMode\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_ac_temperatureSetting_verify(self, valueDict):
        ##  Check data retrieval air conditioner - temperatureSetting of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "temperatureSetting":
                    valueList.append(data['results'][i])
            print("Scope - \"temperatureSetting\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_ac_airFlow_verify(self, valueDict):
        ##  Check data retrieval air conditioner - airFlow of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "airFlow":
                    valueList.append(data['results'][i])
            print("Scope - \"airFlow\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == valueDict['system_value']:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_tp_body_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Data Acquirement - Data Retrieval - Thermo pixi
        ##
        ##  Required parameters:
        ##      uuid                - Device UUID
        ##
        ##  Request body:
        ##  {
        ##      "queries": [
        ##          {
        ##              "deviceUuid": "{device UUID}",
        ##              "scopes": [
        ##                  "battery"
        ##                  "click",
        ##                  "temperature",
        ##                  "humidity"
        ##              ]
        ##          }
        ##      ],
        ##      "time": {
        ##          "startTime": {Timestamp 15 minutes ago},
        ##          "endTime": {Current timestamp}
        ##      },
        ##      "maxCount": 120,
        ##      "offset": 0
        ##  }
        ##
        try:
            body = "{" + \
                "\"queries\": [" + \
                "{" + \
                "\"deviceUuid\": \"" + valueDict['uuid'] + "\"," + \
                "\"scopes\": [" + \
                "\"battery\"," + \
                "\"click\"," + \
                "\"temperature\"," + \
                "\"humidity\"" + \
                "]" + \
                "}" + \
                "]," + \
                "\"time\": {" + \
                "\"startTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time() - 900)) + "," + \
                "\"endTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time())) + "" + \
                "}," + \
                "\"maxCount\": 120," + \
                "\"offset\": 0" + \
                "}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
    
    def data_retrieval_tp_battery_verify(self, valueDict):
        ##  Check data retrieval thermo pixi - battery of HTTP response.
        ##  All value must between "system_value".
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##          format: {minimum value};{maximum value}
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "battery":
                    valueList.append(data['results'][i])
            print("Scope - \"battery\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if int(item['value']) >= int(system_value[0]) and int(item['value']) <= int(system_value[1]):
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_tp_click_verify(self, valueDict):
        ##  Check data retrieval thermo pixi - click of HTTP response.
        ##  All value must be "true" or "false".
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##          format: {minimum value};{maximum value}
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "click":
                    valueList.append(data['results'][i])
            print("Scope - \"click\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if item['value'] == "true" or item['value'] == "false":
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_tp_temperature_verify(self, valueDict):
        ##  Check data retrieval thermo pixi - temperature of HTTP response.
        ##  All value must between "system_value".
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##          format: {minimum value};{maximum value}
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "temperature":
                    valueList.append(data['results'][i])
            print("Scope - \"temperature\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if float(item['value']) >= float(system_value[0]) and float(item['value']) <= float(system_value[1]):
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_tp_humidity_verify(self, valueDict):
        ##  Check data retrieval thermo pixi - humidity of HTTP response.
        ##  All value must between "system_value".
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##          format: {minimum value};{maximum value}
        ##      criteria        - Check condition
        ##        
        try:
            system_value = valueDict['system_value'].split(";")
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "humidity":
                    valueList.append(data['results'][i])
            print("Scope - \"humidity\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                if float(item['value']) >= float(system_value[0]) and float(item['value']) <= float(system_value[1]):
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_body_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Data Acquirement - Data Retrieval - Smart meter
        ##
        ##  Required parameters:
        ##      uuid                - Device UUID
        ##
        ##  Request body:
        ##  {
        ##      "queries": [
        ##          {
        ##              "deviceUuid": "{device UUID}",
        ##              "scopes": [
        ##                  "instanceElectricity",
        ##                  "instanceCurrents",
        ##                  "instanceCurrentsT",
        ##                  "normalUsage",
        ##                  "reverseUsage",
        ##                  "ed",
        ##                  "rssi"
        ##              ]
        ##          }
        ##      ],
        ##      "time": {
        ##          "startTime": {Timestamp 45 minutes ago},
        ##          "endTime": {Current timestamp}
        ##      },
        ##      "maxCount": 500,
        ##      "offset": 0
        ##  }
        ##
        try:
            body = "{" + \
                "\"queries\": [" + \
                "{" + \
                "\"deviceUuid\": \"" + valueDict['uuid'] + "\"," + \
                "\"scopes\": [" + \
                "\"instanceElectricity\"," + \
                "\"instanceCurrents\"," + \
                "\"instanceCurrentsT\"," + \
                "\"normalUsage\"," + \
                "\"reverseUsage\"," + \
                "\"ed\"," + \
                "\"rssi\"" + \
                "]" + \
                "}" + \
                "]," + \
                "\"time\": {" + \
                "\"startTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time() - 2700)) + "," + \
                "\"endTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time())) + "" + \
                "}," + \
                "\"maxCount\": 500," + \
                "\"offset\": 0" + \
                "}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
    
    def data_retrieval_sm_instanceElectricity_verify(self, valueDict):
        ##  Check data retrieval Smart meter - instanceElectricity of HTTP response.
        ##  All value must be a integer number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "instanceElectricity":
                    valueList.append(data['results'][i])
            print("Scope - \"instanceElectricity\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("^(\d+)$", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: integer")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_instanceCurrents_verify(self, valueDict):
        ##  Check data retrieval Smart meter - instanceCurrents of HTTP response.
        ##  All value must be a float number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "instanceCurrents":
                    valueList.append(data['results'][i])
            print("Scope - \"instanceCurrents\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("(\d+\.\d+)", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: float")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_instanceCurrentsT_verify(self, valueDict):
        ##  Check data retrieval Smart meter - instanceCurrentsT of HTTP response.
        ##  All value must be a float number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "instanceCurrentsT":
                    valueList.append(data['results'][i])
            print("Scope - \"instanceCurrentsT\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("(\d+\.\d+)", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: float")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_normalUsage_verify(self, valueDict):
        ##  Check data retrieval Smart meter - normalUsage of HTTP response.
        ##  All value must be a float number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "normalUsage":
                    valueList.append(data['results'][i])
            print("Scope - \"normalUsage\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("(\d+\.\d+)", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: float")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_reverseUsage_verify(self, valueDict):
        ##  Check data retrieval Smart meter - reverseUsage of HTTP response.
        ##  All value must be a float number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "reverseUsage":
                    valueList.append(data['results'][i])
            print("Scope - \"reverseUsage\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("(\d+\.\d+)", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: float")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_ed_verify(self, valueDict):
        ##  Check data retrieval Smart meter - ed of HTTP response.
        ##  All value must be an integer number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "ed":
                    valueList.append(data['results'][i])
            print("Scope - \"ed\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("^(\d+)$", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: integer")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_retrieval_sm_rssi_verify(self, valueDict):
        ##  Check data retrieval Smart meter - rssi of HTTP response.
        ##  All value must be an integer number.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueList = []
            for i in range(len(data['results'])):
                if data['results'][i]['scope'] == "rssi":
                    valueList.append(data['results'][i])
            print("Scope - \"rssi\": ", valueList)
            result = False
            resultList = []
            for item in valueList:
                resultList.append(item['value'])
                match = re.search("^(\d+)$", item['value'])
                if match:
                    result |= True
                else:
                    result &= False
                    break
            print("Actual result: ", resultList, "\nExpected result: integer")
        except:
            raise error.nonamevalue()
        
        try:
            valueDict['value'] = result
            valueDict['system_value'] = True
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def upload_interval_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Gateway Management  - Upload Interval
        ##
        ##  Required parameters:
        ##      gateway_pid         - Gateway ID
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint        - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/gateways/" + dicParam['gateway_pid'] + "/configs"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
   
    def upload_interval_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Gateway Management  - Upload Interval
        ##
        ##  Required parameters:
        ##      token               - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = '%s' % (valueDict['token'])
            header = "{\"accept\": \"application/json\"," + \
                "\"X-ND-TOKEN\": \"" + authValue + "\"," + \
                "\"content-type\": \"application/json\"" + \
                "}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
    
    def upload_interval_body_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Gateway Management  - Upload Interval
        ##
        ##  Required parameters:
        ##      interval            - Upload interval, 1~10
        ##
        ##  Request body:
        ##  {
        ##      "uploadInterval": {interval}
        ##  }
        ##
        try:
            body = "{" + \
                "\"uploadInterval\": " + valueDict['interval'] + \
                "}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
    
    def random_integer_get(self, valueDict):
        ##  Return the random integer.
        ##
        ##  Required parameters:
        ##      minimum         - The minimum of range.
        ##      maximum         - The maximum of range.
        ##      except_number   - The except number.
        ##
        try:
            except_number = int(valueDict['except_number'])
            minimum = int(valueDict['minimum'])
            maximum = int(valueDict['maximum'])
        except:
            raise error.nonamevalue()
        
        ran = except_number
        while ran == except_number:
            ran = random.randint(minimum, maximum)
        print("Random integer: ", ran)
        return ran
    
    def upload_interval_verify(self, valueDict):
        ##  Check upload interval of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            valueDict['value'] = str(data['uploadInterval'])
            print("Actual result: ", valueDict['value'], "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def device_control_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Device Operation - Device Control
        ##
        ##  Required parameters:
        ###     uuid            - Device UUID
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint    - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/devices/" + dicParam['uuid'] + "/control"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
   
    def device_control_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Device Operation - Device Control
        ##
        ##  Required parameters:
        ##      token           - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = valueDict['token']
            header = "{\"accept\": \"application/json\"," + \
                "\"X-ND-TOKEN\": \"" + authValue + "\"," + \
                "\"content-type\": \"application/json\"" + \
                "}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
    
    def device_control_sb_body_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Device Operation - Device Control - ECN Storage battery
        ##
        ##  Required parameters:
        ##      scope               - Scope list, separated by ";"
        ##      scope_value         - Scope value list, separated by ";"
        ##
        ##  Request body:
        ###	{       
        ###		"scopes": [
        ###		    {"{scope 1}": "{scope 1 value}"},
        ###		    {"{scope 2}": "{scope 2 value}"},
        ###         ...
        ###		]
        ###	}
        ##
        try:
            scope = valueDict['scope'].split(";")
            scope_value = valueDict['scope_value'].split(";")
            body = "{\"scopes\": ["
            for i in range(len(scope)):
                body += "{\"" + scope[i] + "\": \""+ scope_value[i] + "\"},"
            body = body[0:len(body) - 1]
            body += "]}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
    
    def device_control_sb_response_verify(self, valueDict):
        ##  Check response of HTTP response.
        ##
        ##  Required parameters:
        ##      value           - JSON data from HTTP response
        ##      system_value    - Expected result
        ##      criteria        - Check condition
        ##        
        try:
            data = eval(valueDict['value'])
            data = json.dumps(data)
            data = json.loads(data)
            del data['statusCode']
            valueDict['value'] = str(data)
            print("Actual result: ", valueDict['value'], "\nExpected result: ", valueDict['system_value'])
        except:
            raise error.nonamevalue()
        
        try:
            Verify().verify(valueDict)
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
    
    def data_callback_verify(self, valueDict):
        ## There are more than one data in data_callback response
        ## step:
        ## Get how many data in the response
        ## verify the data which keys are correct and no missing
        ## Required parameters:
        ##    callbackData    -    Which comes form query_data_get func.
        ##    requestBodyKey  -    ["deviceUuid", "model", "scope", "value", "generatedTime", "uploadedTime"]
        dicParam = dict(valueDict)
        rawData = eval(dicParam["callbackData"])
        listAllQueryScope = []
        requestBodyKey = ["deviceUuid","model","scope","value","generatedTime","uploadedTime"]
        try:
            intDataLen = len(rawData)
            print("total data: {}".format(intDataLen))
            if intDataLen == 0:
                print("No data")
                raise error.notfind()
            else:
                pass
            for i in range(intDataLen):
                clsDataKeyValue = rawData[i][0]["data"][0].keys()
                listDataKeyValue = list(clsDataKeyValue)
                print(listDataKeyValue)
                for x in range(len(listDataKeyValue)):
                    if listDataKeyValue[x] in requestBodyKey:
                        pass
                    else:
                        raise error.notequalerror()
                print(rawData[i][0]["data"][0]["scope"])
                listAllQueryScope.append(rawData[i][0]["data"][0]["scope"])
            if dicParam["scope"] in listAllQueryScope:
                pass
            else:
                raise error.notequalerror()
        except:
            raise error.notfind()

        
    def query_data_get(self, valueDict):
        ## Query data
        ## str_target_table: Table name
        ## str_select_item_sql: Input the table cloumn
        ## str_query_start_time: Get data after str_query_start_time
        ## str_query_start_time: One minute before the current time
        ## Required parameters:
        ## str_select_item_sql    -    received_data
        ## str_table_name         -    datahook
        ## str_ordering_column    -    created_on
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            str_select_item_sql = dicParam["str_select_item_sql"]
            str_target_table = dicParam["str_table_name"]
            str_ordering = dicParam["str_ordering_column"]
            str_query_start_time = (datetime.datetime.now() + datetime.timedelta(minutes = -int(dicParam["timeDelta"])) + datetime.timedelta(hours = -8)).strftime("%Y-%m-%d %H:%M:%S")
            str_sql_cmd = "SELECT {0} FROM {1} WHERE {2} >= '{3}' order by {2} desc".format(str_select_item_sql, str_target_table, str_ordering, str_query_start_time)
            print(str_sql_cmd)
            self.cursor.execute(str_sql_cmd)
            list_results = self.cursor.fetchall()
            for list_no in range(len(list_results)):
                print("Data {}: {}".format((list_no + 1), list_results[list_no]))
                print(type(list_results[list_no]))
            print(type(list_results))
            return list_results
        except Exception as e:
            print("=====> Exception")
            print(e)
            raise error.equalerror()        
        
    def data_upload_api_get(self, valueDict):
        ## Desc.
        ## Uses upload_data, get_token, create_data func.
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
                
        token = self.get_token(dicParam["cube_uuid"])
        json_data = json.dumps(self.create_data(dicParam["device_uuid"], dicParam["data_uuid"],dicParam["data_value"]))
        self.upload_data(token, dicParam["cube_uuid"], json_data)
        
        
    def upload_data(self, token, cube_uuid , json_data):
        qa_std = "https://device-data-qa.nextdrive.io/v1/devices/records"
        headers = {'Content-Type': 'application/json' , 'nextdrive-uuid' : cube_uuid , 'nextdrive-session' : token}
        print(type(json_data))
        r = requests.post(qa_std, data = json_data , headers = headers )
        #r = requests.post(qa_std, json = json_data)
        print("=============")
        print(r.text)
        print(qa_std)
        print("header: ")
        print(headers)
        #print(type(headers))
        print("body: ")
        print(json_data)
        #print(type(json_data))
        print("=============")

        
    def get_token(self, cube_uuid):
        #open file or .......get by self
        request_header = {'authorization': '4581qalink_nxd^_^7w'}
        response = requests.get(("https://tools-qa.nextdrive.io/qa/v1/session/uuid/xxxx/expiration/4").replace("xxxx",cube_uuid) , headers = request_header)
        ret = response.json()
        return(ret['data']['session'])
    
    def create_data(self, device_uuid, data_uuid, data_value):
    
        dataarray = []
        timestamp = int(datetime.datetime.now().timestamp() * 1000)

        value = data_value
        data = {"device_uuid" : device_uuid , 
                         "data_uuid" : data_uuid,
                         "value" : value,
                         "raw_value" : "AAAAAAAAAAHuPleEzJ7exdldie",
                         "tags" : "",
                         "generated_time" : timestamp
                         }
    
        dataarray.append(data)
        jsondata =  { "data" : dataarray }   
        #print(type(jsondata))   
        data = json.dumps(jsondata)
        return jsondata
    
    def device_data_acquire_url_get(self, valueDict):
        ##  Return the HTTP request URL for - 
        ##      Device Operation - Device Data Acquire
        ##
        ##  Required parameters:
        ###     uuid            - Device UUID
        ##      
        ##  Required parameters(conf):
        ##      api_endpoint    - API endpoint
        ##      
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            url = dicParam['api_endpoint'] + "v1/devices/" + dicParam['uuid'] + "/acquire"
            print("HTTP request URL: ", url)
        except:
            raise error.nonamevalue()
        return url
        
    def device_data_acquire_header_get(self, valueDict):
        ##  Return the HTTP request header for - 
        ##      Device Operation - Device Data Acquire
        ##
        ##  Required parameters:
        ##      token           - Oauth token
        ##
        try:
            #authValue = '%s %s' % ('Bearer', valueDict['token'])
            authValue = valueDict['token']
            header = "{\"accept\": \"*/*\"," + \
                "\"X-ND-TOKEN\": \"" + authValue + "\"," + \
                "\"content-type\": \"application/json\"" + \
                "}"
            print("HTTP request header: ", header)
        except:
            raise error.nonamevalue()
        return header
        
    def device_data_acquire_sb_body_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Device Operation - Device Data Acquire - ECN Storage battery
        ##
        ##  Required parameters:
        ##      scope               - Scope list, separated by ";"
        ##
        ##  Request body:
        ###    {       
        ###        "scopes": [
        ###            "{scope 1}",
        ###            "{scope 2}",
        ###         ...
        ###        ]
        ###    }
        ##
        try:
            scope = valueDict['scope'].split(";")
            body = "{\"scopes\": ["
            for i in range(len(scope)):
                body += "\"" + scope[i] + "\","
            body = body[0:len(body) - 1]
            body += "]}"
            print("HTTP request body: ", body)
        except:
            raise error.nonamevalue()
        return body
        
    def string_replace_get(self, valueDict):
        ##  Return the replace string.
        ##  Replace #value_before# to #value_after#.
        ##
        ##  Required parameters:
        ##      value               - Source value.
        ##      value_before        - The string which will be replaced.
        ##      value_after         - The string that #value_before# will be.
        ##
        try:
            print("value before:", valueDict["value"])
            value = re.sub(valueDict['value_before'], valueDict['value_after'], valueDict['value'])
            print("value: ", value)
        except:
            raise error.nonamevalue()
        return value
        
    def nd_token_url_get(self, valueDict):
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            oauth_token_url = ""
            if dicParam['environment'] == "qa":
                oauth_token_url = dicParam['oauth_token_url_qa']
            elif dicParam['environment'] == "production":
                oauth_token_url = dicParam['oauth_token_url_production']
            elif dicParam['environment'] == "development":
                oauth_token_url = dicParam['oauth_token_url_development']
            print("Oauth token URL:", oauth_token_url)
            return oauth_token_url
        except Exception as e:
            print(e)
            raise error.onqaserror()  
    '''            
    def nd_token_header_get(self, valueDict):
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        ##  Create HTTP request headers
        authValue = '%s:%s' % (dicParam['client_id'], dicParam['secret_key'])
        authValue = authValue.encode('utf-8')
        print("before b64encode")
        print(authValue)
        authValue = base64.b64encode(authValue)
        authValue = '%s %s' % ('Basic', authValue.decode('utf-8'))
        HTTPHeader = { \
            'authorization': authValue, \
            'content-type': 'application/x-www-form-urlencoded' \
            }
        
        return HTTPHeader
    '''
    def nd_token_body_get(self, valueDict):
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            oauth_token_url = ""
            oauth_scope = ""
            if dicParam['environment'] == "qa":
                oauth_token_url = dicParam['oauth_token_url_qa']
                oauth_scope = dicParam['api_suffix_qa']
            elif dicParam['environment'] == "production":
                oauth_token_url = dicParam['oauth_token_url_production']
                oauth_scope = dicParam['api_suffix_production']
            elif dicParam['environment'] == "development":
                oauth_token_url = dicParam['oauth_token_url_development']
                oauth_scope = dicParam['api_suffix_development']
            
            if dicParam['scope'] == "User Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_user_management']
            elif dicParam['scope'] == "Gateway Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_gateway_management']
            elif dicParam['scope'] == "Data Acquirement":
                oauth_scope = oauth_scope + dicParam['oauth_scope_data_acquirement']
            elif dicParam['scope'] == "Device Management":
                oauth_scope = oauth_scope + dicParam['oauth_scope_device_management']
            elif dicParam['scope'] == "NextDrive Data Application":
                oauth_scope = oauth_scope + dicParam['oauth_scope_data_application']
            ##  Create HTTP request body
            HTTPBody = { \
                'grant_type': 'client_credentials', \
                'scope': oauth_scope \
                }
            return HTTPBody
        except Exception as e:
            print(e)
            raise error.onqaserror() 
    '''
    def HTTP_nd_token_POST_response_get(self, valueDict):
        ##  HTTP request by POST method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters :
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        requestTimeout = 180
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}

        try:
            dicHeader = dicParam['header']
            print(dicHeader)
            print(type(dicHeader))
            dicHeader = eval(dicHeader)
            dicBody = dicParam['body']
            dicBody = eval(dicBody)
            HTTPResponse = requests.post(dicParam['url'], headers = dicHeader, data = dicBody, timeout = requestTimeout)
            statusCode = HTTPResponse.status_code
            HTTPResponse = HTTPResponse.json()
            print("HTTP status code: ", statusCode)
            print("HTTP response: ", HTTPResponse)
            HTTPResponse['statusCode'] = statusCode
            return HTTPResponse
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
    '''


    def nd_token_header_get(self, valueDict):
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        ##  Create HTTP request headers
        authValue = '%s:%s' % (dicParam['client_id'], dicParam['secret_key'])        
        HTTPHeader = { \
            'authorization': "authValue", \
            'content-type': 'application/x-www-form-urlencoded' \
            }
        
        return HTTPHeader,authValue
        
    
    def HTTP_nd_token_POST_response_get(self, valueDict):
        ##  HTTP request by POST method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters :
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        requestTimeout = 180
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}

        try:
            dicHeaderInfo = dicParam['header']
            dicHeaderInfo = eval(dicHeaderInfo)
            dicHeader = dicHeaderInfo[0]
            authValue = dicHeaderInfo[1]
            authValue = authValue.encode('utf-8')
            authValue = base64.b64encode(authValue)
            authValue = '%s %s' % ('Basic', authValue.decode('utf-8'))
            strHeader = str(dicHeader)
            strHeader = strHeader.replace("authvalue", authValue)
            dicHeader = eval(strHeader)
            dicBody = dicParam['body']
            dicBody = eval(dicBody)
            HTTPResponse = requests.post(dicParam['url'], headers = dicHeader, data = dicBody, timeout = requestTimeout)
            statusCode = HTTPResponse.status_code
            HTTPResponse = HTTPResponse.json()
            print("HTTP status code: ", statusCode)
            print("HTTP response: ", HTTPResponse)
            HTTPResponse['statusCode'] = statusCode
            return HTTPResponse
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()


      
       
    def data_retrieval_single_scope_get(self, valueDict):
        ##  Return the HTTP request body for - 
        ##      Data Acquirement - Data Retrieval - Smart meter
        ##
        ##  Required parameters:
        ##      uuid                - Device UUID
        ##      data_scope          - data_type
        ##
        ##  Request body:
        ##  {
        ##      "queries": [
        ##          {
        ##              "deviceUuid": "{device UUID}",
        ##              "scopes": [
        ##                  "{data_type}"
        ##              ]
        ##          }
        ##      ],
        ##      "time": {
        ##          "startTime": {Timestamp 45 minutes ago},
        ##          "endTime": {Current timestamp}
        ##      },
        ##      "maxCount": 500,
        ##      "offset": 0
        ##  }
        ##    
        dicParamConf = self.configFileParser()
        dicParamIni = dict(valueDict)
        dicParam = {**dicParamConf, **dicParamIni}
        try:
            body = "{" + \
                "\"queries\": [" + \
                "{" + \
                "\"deviceUuid\": \"" + dicParam['uuid'] + "\"," + \
                "\"scopes\": [" + \
                "\"" + dicParam["scope_value"] + "\""\
                "]" + \
                "}" + \
                "]," + \
                "\"time\": {" + \
                "\"startTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time() - 3660)) + "," + \
                "\"endTime\": " + (lambda x: (x.split("."))[0] + "000")(str(time.time())) + "" + \
                "}," + \
                "\"maxCount\": 500," + \
                "\"offset\": 0" + \
                "}"
        except:
            raise error.nonamevalue()
        return body