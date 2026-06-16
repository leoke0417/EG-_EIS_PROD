#coding=utf-8
"""
Created on 2021/09/08
@author     : Dustin Lin
Project     : Postman & Automan Integration
"""

"""
Required

Install:

    Node.js
    Newman(npm install newman -global)
    Newman csv reporter(npm install newman-reporter-csv -global)
    
In postman request:
    "TEST" column need to add the command below:
      
    var body = JSON.parse(responseBody); 
    var content = responseBody;
    tests["Response Body"+content]= body.length != 0

"""
 
import os
import sys
import csv
import json
import automan.tool.error as error 

class postman(object):
    def __init__(self):  
        self.original_path = os.getcwd()
        pass
    
    def command_get(self, dic_value):
        ##  Set postman command
        ##
        ## Required parameters:
        ##      collection      -   Specify a Postman collection as a JSON [file]
        ##      environment     -   Specify a Postman environment as a JSON [file]
        ##      iterations      -   Define the number of iterations to run
        ##
        ## Reference
        ## https://www.itread01.com/content/1514438546.html
        ##
        command = "newman run " + dic_value['collection']
        try:
            dic_value['collection'] in locals().keys()
            dic_key = dic_value.keys()
        except:
            raise error.nonamevalue()
            
        try:
            if "environment" in dic_key:
                command = command + " -e " + dic_value['environment']
            if "iterations" in dic_key:
                command = command + " -n " + dic_value['iterations']
            command = command + " -r csv --reporter-csv-export"
        except:
            raise error.notfind()
        
        print(command)
        return command
        
    def command_exec(self, dic_value):
        ## Run postman command line
        ##
        ## Required parameters
        ##      command
        ##
        ## Note:
        ##      location of report saved: /postman/newman
        try:
            dic_value['command'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            os.chdir(os.path.join(self.original_path, "postman"))
            os.system(dic_value['command'])
            os.chdir(self.original_path)
        except:
            raise error.notfind()
           
    def result_get(self):
        ## Get result of execution
        ##
        ## Required parameters
        ##
        try:
            str_path = os.path.join(self.original_path, "postman", "newman")
            #print(str_path)
            list_file_name = os.listdir(str_path)
            str_target_file_name = list_file_name[-1]
            #print(list_file_name)
            #print(str_target_file_name)
        except:
            raise error.notfind()
        return str_target_file_name

    def read_csv_get(self, dic_value):
        ## Read csv file
        ##
        ## Required parameters
        ##      filename    - csv file name
        try:
            dic_value['filename'] in locals().keys()
            max_int = sys.maxsize
        except:
            raise error.nonamevalue()
            
        while True:
            # decrease the maxInt value by factor 10 
            # as long as the OverflowError occurs.
            try:
                csv.field_size_limit(max_int)
                break
            except OverflowError:
                max_int = int(max_int/10)
        
        try:
            str_path = os.path.join(self.original_path, "postman", "newman", dic_value['filename'])
            # list_data -> to store csv content by line
            list_data = []
            with open(str_path, newline = "", encoding = "utf-8") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    list_data.append(row)

            # Delete first line(title) of the csv:
            del list_data[0]
        except:
            raise error.notfind()
        return list_data
    
    def find_result_get(self, dic_value):
        ## Find the target result
        ##
        ## Required parameters:
        ##      testcase - testcase title
        ##      file    -   result content
        try:
            dic_value['file'] in locals().keys()
            dic_value['testcase'] in locals().keys()
            dic_value['file'] = eval(dic_value['file'])
            # str_target_data -> to store the specific data
            str_target_data = []
        except:
            raise error.nonamevalue()

        try:
            for data_no in range(len(dic_value['file'])):
                if dic_value['testcase'] in dic_value['file'][data_no]:
                    str_target_data.append(dic_value['file'][data_no])
                else:
                    pass
        except:
            raise error.notfind()
        return (str_target_data)
        
    def api_result_get(self, dic_value):
        ## Get status code and response body, stored in tuple
        ##
        ## Required parameters:
        ##      api_result
        ##
        ## Result format:
        ## result = []
        ## [["status code 1", "response body 1"], ["status code 2", "response body 2"]]
        try:
            dic_value['api_result'] in locals().keys()
            list_response = eval(dic_value['api_result'])
            result = []
        except:
            raise error.nonamevalue()
        try:
            if len(list_response) > 1:       
                ## iterations > 1
                for i in range(len(list_response)):
                    result.append([])
                    result[i].append(list_response[i][6])
                    # if did not setup to get response body in postman
                    if len(list_response[i]) <= 9:
                        result[i].append("No response body")
                    else:
                        result[i].append(list_response[i][9].replace("Response Body", ""))
            else:
                print(list_response)
                result.append(list_response[0][6])
                # if did not setup to get response body in postman
                if len(list_response[0]) <= 9:
                    result.append("No response body")
                else:
                    result.append(list_response[0][9].replace("Response Body", ""))
        except:
            raise error.notfind()
        return result
        
    def status_code_verify(self, dic_value):
        ## Verify status code from api response
        ## Parameters:
        ##      api_result
        ##      expected_result
        ##
        try:
            dic_value['api_result'] in locals().keys()
            list_api_result = eval(dic_value['api_result'])
            list_status_code = []
        except:
            raise error.nonamevalue()
        
        try:
            if isinstance(list_api_result[0], list):
                ## if iterations > 1
                for i in range(len(list_api_result)):
                    list_status_code.append(list_api_result[i][0])
            else:
                list_status_code.append(list_api_result[0])
        except:
            raise error.notfind()
                  
        for i in range(len(list_status_code)):
            if dic_value["expected_result"] == list_status_code[i]:
                pass
            else:
                print(list_status_code[i])
                raise error.equalerror()

        
        
    def postman_json_get(self, dic_value):
        ## To get postman json file content
        ##
        ##  Required parameters:
        ##      json_name
        try:
            dic_value["json_name"] in locals().keys()
        except:
            raise error.nonamevalue()
            
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "r", encoding = "utf-8")
        file = f.read()
        f.close()
        return file

    def postman_json_get(self, dic_value):
        ## To get postman json file content
        ##
        ##  Required parameters:
        ##      json_name
        try:
            dic_value["json_name"] in locals().keys()
        except:
            raise error.nonamevalue()

        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "r", encoding="utf-8")
        file = f.read()
        f.close()
        return file

    def postman_json_set(self, dic_value):
        ## In order to change postman json body
        ##
        ## Required Parameters:
        ##      json_name
        ##      json_content
        ##
        try:
            dic_value["json_content"] in locals().keys()
            dic_value["json_name"] in locals().keys()
        except:
            raise error.nonamevalue()

        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(dic_value["json_content"])
        f.close()

    def postman_environment_set(self, dic_value):
        json_file = json.loads(dic_value["environment"])
        str_access_token = eval(dic_value["access_token"])[0]
        # print(str_access_token)
        # print(json_file)
        # print(type(json_file))
        # print(type(json_file["values"]))

        for i in range(len(json_file["values"])):
            if json_file["values"][i]["key"] == dic_value["target_key"]:
                print(i)
                json_file["values"][i]["value"] = str_access_token
            else:
                pass

        # print(json_file)
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(json.dumps(json_file))
        f.close()

    def postman_access_token_set(self, dic_value):
        json_file = json.loads(dic_value["environment"])
        str_access_token = dic_value["access_token"]
        # print(str_access_token)
        # print(json_file)
        # print(type(json_file))
        # print(type(json_file["values"]))

        for i in range(len(json_file["values"])):
            if json_file["values"][i]["key"] == dic_value["target_key"]:
                print(i)
                json_file["values"][i]["value"] = str_access_token
            else:
                pass

        # print(json_file)
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(json.dumps(json_file))
        f.close()
        
    def postman_device_uuid_set(self, dic_value):
        json_file = json.loads(dic_value["environment"])
        str_device_uuid = dic_value["devices_uuid"]
        print(str_device_uuid)
        print(json_file)
        # print(type(json_file))
        # print(type(json_file["values"]))

        for i in range(len(json_file["values"])):
            if json_file["values"][i]["key"] == dic_value["device_uuid"]:
                json_file["values"][i]["value"] = str_device_uuid
            else:
                pass

        print(json_file)
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(json.dumps(json_file))
        f.close()
        
        
    def postman_data_uuid_set(self, dic_value):
        json_file = json.loads(dic_value["environment"])
        str_data_uuid = dic_value["datas_uuid"]
        print(str_data_uuid)
        print(json_file)
        # print(type(json_file))
        # print(type(json_file["values"]))

        for i in range(len(json_file["values"])):
            if json_file["values"][i]["key"] == dic_value["data_uuid"]:
                json_file["values"][i]["value"] = str_data_uuid
            else:
                pass

        print(json_file)
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        f = open(file_path, "w", encoding="utf-8")
        f.write(json.dumps(json_file))
        f.close()
        

        