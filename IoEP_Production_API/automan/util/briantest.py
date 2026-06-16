
import json 
import os
import sys
import csv
import automan.tool.error as error 

class briantest(object):
    def __init__(self):  
        self.original_path = os.getcwd()
        pass
    
    def update_app_labels_new_id_get(self, dic_value):
        ## for PUT, DELETE app-labels
        ## add uuid to url
        ##
        ## Required parameters
        ##      collection_content
        ##      app_label_uuid
        ##
        try:
            dic_value["cc"] in locals().keys()
            dic_value["new_id"] in locals().keys()
            tuple_new_param = eval(dic_value["new_id"])
        except:
            raise error.nonamevalue()
        try:
            json_content = json.loads(dic_value["cc"])
            json_content["item"][1]["request"]["url"]["raw"] = tuple_new_param[0]
            json_content["item"][1]["request"]["url"]["path"] = tuple_new_param[1]
            json_file = json.dumps(json_content)
        except:
            raise error.notfind()
        
        return json_file

    
    def update_id_url_get(self, dic_value):
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
        
        
        
        
      
    
        

               