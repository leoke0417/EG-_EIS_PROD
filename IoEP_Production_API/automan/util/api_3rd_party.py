#coding=utf-8
"""
Created on 2021/09/29

@author: Dustin Lin
"""

import automan.tool.error as error
import time
import os
import json


class api_3rd_party(object):
    def __init__(self):
        pass
    
    def data_acquirement_body_get(self, dic_value):
        ## generate data acquirement request body to change postman collection file
        ##
        ## Required parameter:
        ##      device_uuid
        ##      scope
        ##
        try:
            dic_value["device_uuid"] in locals().keys()
            dic_value["scope"] in locals().keys()
            end_time = str(round(time.time()*1000))
            start_time = str(int(end_time) - 10800000)
            # start_time: 3 hours before end_time
        except:
            raise error.nonamevalue()
        
        try:
            body = "{\"queries\": [{\"deviceUuid\": \"" + dic_value["device_uuid"] + "\"," + \
                    "\"scopes\": [\"" + dic_value["scope"] + "\"]}]," + \
                    "\"time\":{ \"startTime\": " + start_time + \
                    "," + "\"endTime\": " + end_time + \
                    "}, \"maxCount\": 50, \"offset\": 0}"
        except:
            raise error.notfind()
        return body
        
    def data_acquirement_new_body_get(self, dic_value):
        ## To change request body of API
        ##
        ## Required parameters
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
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file
 
        
        
        
        
        
        
        
        