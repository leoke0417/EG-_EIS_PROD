#coding=utf-8
"""
Created on 2021/05/06
@author     : Dustin Lin
Project     : Postman Automan Integration
"""
import automan.tool.error as error  
import json
import uuid
import requests, base64

class api_egplus_app(object):
    def __init__(self):  
        pass
    
    def ndtoken_get(self, dic_value):
        try:
            dic_value['id_token'] in locals().keys()
            app_uuid = str(uuid.uuid4())           
        except:
            raise error.nonamevalue()
        
        
        try: 
            strExchange_URL = 'https://api-eg3-qa.nextdrive.io/api/v1/oauth2/tokens/exchange'
            dicHeader = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            
            dicBody = {
                    'type': 'cognito',
                    'token': dic_value['id_token'],
                    'appUuid': app_uuid
                }
            jsonBody = json.dumps(dicBody)
            objResponse = requests.post(strExchange_URL, data = jsonBody, headers = dicHeader)
            #print("appUuid => ".format(app_uuid))
            if objResponse.status_code == 200:
                dicResponse = objResponse.json()
                
                return (dicResponse['accessToken'])
            else:
                print("!= 200")
                
        except Exception as exceptionError:
            print("Exception---->")
            print(exceptionError)
    
    def status_code_get(self, dic_value):
        ## Get Status code
        ##
        ## Required parameter:
        ##      api_response
        ##
        try:
            dic_value['api_response'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            api_result = eval(dic_value['api_response'])
            status_code = api_result[1]
            return status_code
        except:
            raise error.notfind()
    
    def response_body_get(self, dic_value):
        ## Get API response body
        ##
        ## Required parameter:
        ##      api_response
        ##
        try:
            dic_value['api_response'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            api_result = eval(dic_value['api_response'])
            response_body = api_result[0]
            return response_body
        except:
            raise error.notfind()
    
    def check_latests_noti_camera_noti_exist_get(self, dic_value):
        ## The response body of the camera is special 
        ## example:
        """
        {
            "events": [
                {
                    "deviceUuid": "31b92857-ed59-47b0-b64e-4a6d9616f22b",
                    "gatewayUuid": "23d5de6a-01b4-4529-ada8-16a913031324",
                    "scope": "camera",
                    "model": "Camera",
                    "params": {
                        "template": "motion_detected_link_with_camera",
                        "cameraUuid": "31b92857-ed59-47b0-b64e-4a6d9616f22b",
                        "cameraName": "Camera"
                    },
                    "triggeredAt": 1627439548564,
                    "value": "true"
                },
                {
                    "deviceUuid": "bf4eb1f2-a31d-46dc-8cba-d3b608b6aed8",
                    "gatewayUuid": "23d5de6a-01b4-4529-ada8-16a913031324",
                    "scope": "click",
                    "model": "Pixi-HT",
                    "params": {
                        "template": "button_clicked"
                    },
                    "triggeredAt": 1627379261562,
                    "value": "true"
                }
            ]
        }
        """
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - model
        ## result:
        ##      - return type: boolean
        ## function:
        ##      - check if camera notification is exist.
        dic_param = dict(dic_value)
        json_file = json.loads(dic_param["response_body"])
        for i in range(len(json_file[dic_param["first_key"]])): 
            print(json_file[dic_param["first_key"]][i][dic_param["second_key"]])
            if json_file[dic_param["first_key"]][i][dic_param["second_key"]] == dic_param["model"]:
                exist_flag = True
                index = i
            else:
                exist_flag = False
        return exist_flag,index

    def latest_noti_camera_value_get(self, dic_value):
        ## The response body of the camera is special 
        ## example:
        """
        {
            "events": [
                {
                    "deviceUuid": "31b92857-ed59-47b0-b64e-4a6d9616f22b",
                    "gatewayUuid": "23d5de6a-01b4-4529-ada8-16a913031324",
                    "scope": "camera",
                    "model": "Camera",
                    "params": {
                        "template": "motion_detected_link_with_camera",
                        "cameraUuid": "31b92857-ed59-47b0-b64e-4a6d9616f22b",
                        "cameraName": "Camera"
                    },
                    "triggeredAt": 1627439548564,
                    "value": "true"
                },
                {
                    "deviceUuid": "bf4eb1f2-a31d-46dc-8cba-d3b608b6aed8",
                    "gatewayUuid": "23d5de6a-01b4-4529-ada8-16a913031324",
                    "scope": "click",
                    "model": "Pixi-HT",
                    "params": {
                        "template": "button_clicked"
                    },
                    "triggeredAt": 1627379261562,
                    "value": "true"
                }
            ]
        }
        """
        ## Parameter:
        ##      - response_body
        ##      - first_key
        ##      - second_key
        ##      - third_key
        ##      - cam_result: ("true" or "false", index)
        ## result:
        ##      - return type: list
        ## function:
        ##      - get params value of camera
        dic_param = dict(dic_value)
        json_file = json.loads(dic_param["response_body"])
        tuple_cam_value = eval(dic_param["cam_result"])
        list_values = []
        if tuple_cam_value[0] is True:
            list_values.append(json_file[dic_param["first_key"]][tuple_cam_value[1]][dic_param["second_key"]][dic_param["third_key"]])
        elif tuple_cam_value[0] is False:
            pass
        else:
            raise error.notfind()
        return list_values
        
    def gateway_associate_url_get(self, dic_value):
        ## Return the HTTP request URL for - 
        ##      Gateway association
        ##
        ## Required parameter(ini):
        ## api_endpoint 
        try:
            dic_value['api_endpoint'] in locals().keys()
        except:
            raise error.nonamevalue
        
        try:
            url = dic_value['api_endpoint'] + "/api/v1/associations/gateways"
            print("HTTP request URL: ", url)
        except:
            raise error.notfind()
        return url
        
    def gateway_associate_header_get(self, dic_value):
        ## Return the HTTP request header for -
        ##      Gateway association
        ##
        ## Required parameter:
        ##      token      - nd token
        try:
            dic_value['nd_token'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            authValue = dic_value['nd_token']
            header = "{\"accept\": \"application/json\"," + \
                     "\"Authorization\": \"Bearer " + authValue + "\"," + \
                     "\"Content-Type\": \"application/json\"}"
            print("HTTP request header: ", header)
        except:
            raise error.notfind()
        return header
        
    def gateway_associate_body_get(self, dic_value):
        ## Return the HTTP request body for - 
        ##      Gateway association
        ##
        ## Required parameter:
        ##  profile_id: gateway uuid
        ##  pid: gateway pid
        ##  name: gateway name
        ##  model: gateway model i.e., Cube or Atto
        ##
        try:
            dic_value['profile_id'] in locals().keys()
            dic_value['pid'] in locals().keys()
            dic_value['name'] in locals().keys()
            dic_value['model'] in locals().keys()
        except:
            raise error.nonamevalue
            
        try:
            body = "{\"profileId\": \"" + dic_value['profile_id'] + "\"," + \
                    "\"pid\": \"" + dic_value['pid'] + "\"," + \
                    "\"name\": \"" + dic_value['name'] + "\"," + \
                    "\"model\": \"" + dic_value['model'] + "\"}" 
            print("HTTP request body: ", body)
        except:
            raise error.notfind()

        return body
        
    
       
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        

     