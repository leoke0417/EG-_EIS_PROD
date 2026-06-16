#coding=utf-8
"""
Created on: 2022/01/17
@author: Dustin
"""
import json
import automan.tool.error as error  

class api_service_store(object):
    def __init__(self):  
        pass
    def update_contracts_url_get(self, dic_value):
        ## To generate new url for delete contract API
        try:
            dic_value["contract_uuid"] in locals().keys()
            list_contract_uuid = eval(dic_value['contract_uuid'])
            contract_uuid = list_contract_uuid[0]
        except:
            raise error.nonamevalue()
        
        try:
            url = "{{end_point}}/manager/providers/1/services/{{TesttServicee_R9B_uuid}}/contracts/" + contract_uuid
            path = [
                        "manager",
                        "providers",
                        "1",
                        "services",
                        "{{TesttServicee_R9B_uuid}}",
                        "contracts",
                        contract_uuid
                    ]
            
        except:
            raise error.notfind()
        return url, path
    
    def update_contracts_new_url_get(self, dic_value):
        ## Set the new url for delete API collection.json
        try:
            dic_value["collection_content"] in locals().keys()
            dic_value["new_param"] in locals().keys()
            tuple_new_param = eval(dic_value["new_param"])
        except:
            raise error.nonamevalue()
        
        try:
            json_content = json.loads(dic_value["collection_content"])
            json_content["item"][0]["request"]["url"]["raw"] = tuple_new_param[0]
            json_content["item"][0]["request"]["url"]["path"] = tuple_new_param[1]
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        return json_file
    
