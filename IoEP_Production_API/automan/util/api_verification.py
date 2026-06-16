#coding=utf-8
"""
Created on 2021/04/15
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
import codecs
import uuid
from ldap3 import strategy
import requests, json


class api_verification(object):
    def __init__(self):  
        self.total = 0
        pass

    def read_csv_get(self, dic_value): 
        ## Read csv file and find the target response
        ##
        ## Parameters:
        ##    - csv_filename
        ##    - testcase_name
        ##
        dic_param = dict(dic_value)
        #print("THIS>>>")
        #print(dic_param)
        maxInt = sys.maxsize
         
        while True:
            # decrease the maxInt value by factor 10 
            # as long as the OverflowError occurs.
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt/10)
        
        try:
        
            #define csv file:
            str_file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"], "newman",dic_param["csv_filename"])
            list_data = []
            str_target_data = ""
            #open csv file and write into a list:
            with open(str_file_path, newline = "", encoding = "utf-8", errors = 'ignore') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    list_data.append(row)
            #delete first line of the csv:
            del list_data[0]
            
            #choose which response data you want:
            for data_no in range(len(list_data)):
                if dic_param["testcase_name"] in list_data[data_no]:
                    str_target_data = list_data[data_no]
                    #print(str_target_data)
                else:
                    pass
            #return response
            return str_target_data
        
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()         
        pass
        
    
    
    def status_code_get(self, dic_value):
        ## Get status code of API response
        ## Parameters:
        ##     - api_response
        ##
        dic_param = dict(dic_value)
        str_response = dic_param["api_response"]
        print(dic_param)
        print("THIS>>>")
        print(str_response)
        print(type(str_response))
        list_response = eval(str_response)
        print(list_response)
        for i in range(len(list_response)):
            if "http" in list_response[i]:
                #print(list_response[i + 2])
                str_status_code = list_response[i + 2]
                break
            else:
                pass
        return str_status_code
            
    def response_body_get(self, dic_value):
        ## Get response body of API response
        ## Parameters:
        ##     - api_response
        ##
        dic_param = dict(dic_value)
        str_response = dic_param["api_response"]
        list_response = eval(str_response)
        #find response body:
        for i in range(len(list_response)):
            if "http" in list_response[i]:
                #To check if has response body:
                if i + 5 >= len(list_response):
                    str_response_body = "No body"
                    print("No body")
                    break
                else:
                    pass
                    #To find the response body:
                    print(list_response[i+5])
                    str_response_body = list_response[i+5]
                    str_response_body = str_response_body.replace("Response Body", "")
                    print(str_response_body)
                return str_response_body
            else:
                pass
    
    def status_code_verify(self, dic_value):
        ## Verify status code from api response
        ## Parameters:
        ##     - api_response
        ##
        dic_param = dict(dic_value)
        #Loading response and transfer to json format:
        str_response = dic_param["api_response"]
        print("THIS>>>>>")
        print(str_response)
        if str_response == dic_param["expected_status_code"]:
            print("Status code: EQUAL")
            pass
        else:
            raise error.equalerror()
        #json_response = json.loads(str_response)
        
    def path_get(self):
        ## Get executed location
        str_path = os.getcwd()
        return str_path
        
    def cmd_path_set(self, dic_value):
        ## Set location
        ## Parameters:
        ##    - environment_path
        ##
        dic_param = dict(dic_value)
        os.chdir(dic_param["environment_path"])
        
    def cmd_exec(self, dic_value):
        ## Executes command
        ## Parameters:
        ##     - command
        ##
        dic_param = dict(dic_value)
        os.chdir(os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"]))
        os.system(dic_param["command"])
        os.chdir(dic_param["original_path"])
        
    def file_list_get(self, dic_value):
        ## Get file list in folder which stored response csv file
        ## Parameters:
        ##     - folder_path
        ##
        dic_param = dict(dic_value)
        print(os.getcwd())
        str_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"], dic_param["folder_path"])
        print(str_path)
        list_file_name = os.listdir(str_path)
        str_target_file_name = list_file_name[-1]
        print(list_file_name)
        print(str_target_file_name)
        return str_target_file_name
    
    
    def expected_result_get(self, dic_value):
        ## Get expected result
        ## Parameters:
        ##     - expected_result
        ##
        dic_param = dict(dic_value)
        str_file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "expected_result", dic_param["environment"], dic_param["expected_result"])
        print(str_file_path)
        
        obj_expected_result = open(str_file_path, "r", encoding = 'utf-8')
        #obj_expected_result = open(str_file_path, "r")
        str_expected_result = obj_expected_result.read()
        #print(str_expected_result)
        obj_expected_result.close()
        
        
        return str_expected_result
    
    def dict_keys_verify(self, dic_value):
        ## Verify dictionary keys
        ## Parameters:
        ##     - expected_result
        ##     - actual_result
        ##
        """
        try:
            dic_param = dict(dic_value)
            dic_expected_result = json.loads(dic_param["expected_result"])
            dic_actual_result = json.loads(dic_param["actual_result"])
            list_expected_keys = list(dic_expected_result.keys())
            list_actual_keys = list(dic_actual_result.keys())
            print("***********************************************")
            print("***********************************************")
            print("Expected result")
            print(dic_expected_result)
            print("Actual result")
            print(dic_actual_result)
            print("***********************************************")
            print("***********************************************")
            print("***********************************************")
            print("Expected keys")
            print(list_expected_keys)
            print("Actual keys")
            print(list_actual_keys)
            print("***********************************************")
            print("***********************************************")
            for i in range(len(list_expected_keys)):
                if list_expected_keys[i] in list_actual_keys:
                    print("Key \"{}\"".format(list_expected_keys[i]).ljust(25) + "exists")
                else:
                    print("missing key: ", list_expected_keys[i])
                    raise error.equalerror()
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()         
        pass
        """
        dic_param = dict(dic_value)


        dic_expected_result = json.loads(dic_param["expected_result"])
        try:
            dic_actual_result = json.loads(dic_param["actual_result"])
        except:
            dic_actual_result = dic_param["actual_result"]
        
        if type(dic_actual_result) == list:
            print("list")
        elif type(dic_actual_result) == dict:
            print("dict")
            try:
                list_expected_keys = list(dic_expected_result.keys())
                list_actual_keys = list(dic_actual_result.keys())
                print("***********************************************")
                print("***********************************************")
                print("Expected result")
                print(dic_expected_result)
                print("Actual result")
                print(dic_actual_result)
                print("***********************************************")
                print("***********************************************")
                print("***********************************************")
                print("Expected keys")
                print(list_expected_keys)
                print("Actual keys")
                print(list_actual_keys)
                print("***********************************************")
                print("***********************************************")
            except:
                raise error.equalerror()
            for i in range(len(list_expected_keys)):
                if list_expected_keys[i] in list_actual_keys:
                    print("Key \"{}\"".format(list_expected_keys[i]).ljust(25) + "exists")
                else:
                    print("missing key: ", list_expected_keys[i])
                    raise error.equalerror()
    
    def dict_content_verify(self, dic_value):
        ### Expected result:
        ###     Get from the API response body
        ### Verifying point:
        ###     value: key value is equal to expected result
        ### Parameter:
        ###     actual_result: json format
        ###     expected_result: json format
        ### API:
        ###     EG+:
        ###         GET_api_v1_users.qa
        try:
            dic_param = dict(dic_value)
            dic_expected_result = json.loads(dic_param["expected_result"])
            dic_actual_result = json.loads(dic_param["actual_result"])
            list_expected_keys = list(dic_expected_result.keys())
            list_actual_keys = list(dic_actual_result.keys())
            print("***********************************************")
            print("***********************************************")
            for i in range(len(list_expected_keys)):
                print("EXPECTED RESULT")
                print(dic_expected_result[list_expected_keys[i]])
                print("=====")
                print("ACTUAL RESULT")
                print(dic_actual_result[list_expected_keys[i]])
                print("=====")
                if dic_expected_result[list_expected_keys[i]] == dic_actual_result[list_expected_keys[i]]:
                    print("Expected result: {}".format(dic_expected_result[list_expected_keys[i]]).ljust(50) + "||" + "Actual result: {}".format(dic_actual_result[list_expected_keys[i]]).rjust(50))
                else:
                    raise error.equalerror()
            print("***********************************************")
            print("***********************************************")
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()         
        pass        
    
    def environment_token_set(self, dic_value):
        ## To change cognito token in environment.json file
        ##
        dic_param = dict(dic_value)
        file_name = dic_param["environment_name"]
        file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"], file_name)
        print(file_path)
        f = open(file_path, "r+")
        file = f.read()
        f.close()
        dic_file = json.loads(file)
        for i in range(len(dic_file["values"])):
            if dic_file["values"][i]["key"] == "cognito_token":
                dic_file["values"][i]["value"] = dic_param["new_token"]
                break
            else:
                pass
        
        new_file = open(file_path, "w")
        new_file.write(json.dumps(dic_file))
        new_file.close()
        
    def collection_token_set(self, dic_value):
        ## To change cognito token in collection.json file
        ##
        dic_param = dict(dic_value)
        file_name = dic_param["collection_name"]
        file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"], file_name)
        target = ""
        target2 = ""
        target3 = ""
        print(file_path)
        f = open(file_path, "r", encoding = "utf-8")
        file = f.read()
        f.close()
        
        dic_file = json.loads(file)
        print(dic_file["item"][0]["name"])
        if dic_file["item"][0]["name"] == dic_param["testcase_name"]:
            target = dic_file["item"][0]["event"][0]["script"]["exec"][12]
            target2 = re.sub(r"^\s+", "", target)
            print(target)
            print("target2")
            print(target2)
        else:
            print("error 1")
        
        if "token" in target2:
            target3 = target2[0:7]
            print("target3")
            print(target3)
        else:
            print("error 2")
        final_target = target3 + "\"" + dic_param["new_token"] + "\","
        dic_file["item"][0]["event"][0]["script"]["exec"][12] = final_target
        print(dic_file)
        json_file = json.dumps(dic_file)
        print("========================================================")
        print(json_file)
        
        file1 = open(file_path, "w")
        file1.write(json_file)
        file1.close()
        
    def id_token_get(self, dic_value): 
        ## will modify, move parameter to ini file
        dic_param = dict(dic_value)
        strAWSRegion = dic_param["pool_id"].split("_")[0]
        str_ID_token = ""
        try:
            client = boto3.client('cognito-idp', region_name=strAWSRegion, config = botocore.client.Config(signature_version = UNSIGNED))
            objAWS = AWSSRP(
                    username = dic_param["username"], 
                    password = dic_param["password"], 
                    pool_id = dic_param["pool_id"], 
                    client_id = dic_param["client_id"], 
                    client = client
                )
            dicToken = objAWS.authenticate_user()
            str_ID_token = dicToken['AuthenticationResult']['IdToken']
            #print(dicToken)
            print("Cognito token")
            print(str_ID_token)
        except Exception as exceptionError:
            #raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            #raise error.equalerror()
            #raise error.equalerror() 
        return str_ID_token
    
    def api_count_get(self):
        self.total = self.total + 1

        final_result = self.total - 1
        
        return final_result
                
    ### Edit date: 07/05/21
    def unix_timestamp_verify(self, dic_value):
        ### Expected result:
        ###     type: int
        ###     value: timestamp, Not null
        ###     len: {actual_result} == 13
        ### Parameter:
        ###     actual_result: [timestamp1, timestamp2, ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        try:
            for i in range(len(list_actual_result)):
                if type(list_actual_result[i]) is int and len(str(list_actual_result[i])) == 13 and list_actual_result[i] != None:pass
        except:
            raise error.equalerror()
        print("\nUnix timestamp comapre result: PASS\n")
        
        
    def battery_verify(self, dic_value):
        ### Expected result: 
        ###     type: string
        ###     value: "0" ~ "100", Not null
        ###     len: 1 <= {actual_result} <= 3
        ### Parameter:
        ###     actual_result: ["battery value 1", "battery_value 2", ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_actual_result)):
            if type(list_actual_result[i]) is str and len(list_actual_result[i]) >= 1 and len(list_actual_result[i]) <= 3 and list_actual_result[i] != None:
                pass
            else:
                raise error.equalerror()
        print("\nBattery value comapre result: PASS\n")
        
    def uuid_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: Only contains "-", "a-z", "A-Z", "0-9"
        ###     len: 36
        ### Parameter:
        ###     actual_result: ["uuid1", "uuid2", ...]
        try:
            dic_param = dict(dic_value)
            list_uuid = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        try:
            for i in range(len(list_uuid)):
                uuid_pattern = re.compile(r'[0-9a-zA-Z-]')
                list_uuid_alphabet = re.findall(uuid_pattern, list_uuid[i])
                int_current_uuid_len = len(list_uuid[i])
                int_compare_result_uuid_len = len(list_uuid_alphabet)
                if int_compare_result_uuid_len == int_current_uuid_len and int_current_uuid_len == 36:
                    pass
                elif int_current_value_len == 0:
                    print("There is a Null vale")
                    pass
                else:
                    raise error.equalerror()
            print("\nUUID compare result: PASS\n")
        except:
            raise error.equalerror()

    def int_verify(self, dic_value):
        ### Expected result:
        ###     type: int
        ###     value: Not null
        ### Parameter:
        ###     actual_result: [int1, int2, ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        print(list_actual_result)
        try:
            for i in range(len(list_actual_result)):
                if type(list_actual_result[i]) is int and list_actual_result[i] != None:
                    pass
        except:
            raise error.equalerror()
        print("\nInteger compare reult: PASS\n")
        
    def float_verify(self, dic_value):
        ### Expected result:
        ###     type: int
        ###     value: Not null
        ### Parameter:
        ###     actual_result: [int1, int2, ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        print(list_actual_result)
        for i in range(len(list_actual_result)):
            if type(list_actual_result[i]) is float and list_actual_result[i] != None:
                pass
            else:
                raise error.equalerror()
        print("\nFloat compare reult: PASS\n")   
            
    def boolean_verify(self, dic_value):
        ### Expected result:
        ###     type: boolean
        ### Parameter:
        ###     actual_result: [bool1, bool2, ...]
        ### API:
        ###     EG+:
        ###         GET_api_v1_devices_{deviceUuid}_notifications.qa
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_actual_result)):
            if list_actual_result[i] == True or list_actual_result[i] == False:
                pass
            else:
                print("Fail!!!\nResult:\n")
                print(list_actual_result[i])
                raise error.equalerror()
        print("\nThe boolean comapre result: PASS\n")

    def value_verify(self, dic_value):
        ### Expected result:
        ###     actual_result == expected_result
        ### Parameter:
        ###     actual_result: $actual_result$
        ###     expected_result: $expected_result$
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        print("\nExpected result: {}   Actual result: {}".format(dic_param["expected_result"], list_actual_result[0]))
        if dic_param["expected_result"] == list_actual_result[0]:
            print("\nTwo value Compare result: Equal\n")
            pass
        else:
            raise error.equalerror()

    def online_status_verify(self, dic_value):
        ### Expected result:
        ###     type: int
        ###     value: 0 or 1 or 2 and Not null
        ### Parameter:
        ###     actual_result: [int1, int2, ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_online_status)):
            if list_online_status[i] == 0 or list_online_status[i] == 1 or list_online_status[i] == 2 and list_online_status[i] != None:
                pass
            else:
                raise error.equalerror()
        print("\nOnline status compare result: PASS\n")
        
    def url_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: Start with "http", Not null
        ### Parameter:
        ###     actual_result: [url1, url2, ...]
        try:
            dic_param = dict(dic_value)
            list_url = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_url)):
            url_pattern = re.compile(r'^http')
            list_url_alphabet = re.findall(url_pattern, list_url[i])
            if len(list_url_alphabet) == 0:
                print("\n")
                print(list_url[i])
                print("\n")
                raise error.equalerror
            else:
                pass
        print("\nURL compare result: PASS\n")

    def device_uuid_verify(self, dict_value):
        try:
            if dict_value["first_uuid"] == dict_value["second_uuid"]:
                print("uuid compare pass")
            else:
                print("uuid compare fail")

        except Exception as exceptError:
            print("=====> Exception: ")
            print(exceptError)
            raise error.equalerror()
        
        
    def string_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: Not null
        ### Parameter:
        ###     actual_result: ["string1", "string2", ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        try:
            for i in range(len(list_actual_result)):
                if type(list_actual_result[i]) is str:
                    pass
        except:
            raise error.equalerror()
        print("\nString compare result: PASS\n")
        
    def string_null_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ### Parameter:
        ###     actual_result: ["string1", "string2", ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_actual_result)):
            if type(list_actual_result[i]) is str:
                pass
            else:
                print("error value: ", list_actual_result[i])
                print(type(list_actual_result[i]))
                if list_actual_result[i] == None:
                    print("type is none")
                else:
                    raise error.equalerror()
        print("\nString compare result: PASS\n")        
    
    def pid_verify(self, dic_value):
        ### Expected result: 
        ###     type: String
        ###     value: Only contain 0-9, capital A-Z, Not Null
        ### Parameter:
        ###     acutal_result: ["PID1", "PID2", ...]
        try:
            dic_param = dict(dic_value)
            list_pid = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_pid)):
            pid_pattern = re.compile(r'[0-9A-Za-z]')
            list_pid_alphabet = re.findall(pid_pattern, list_pid[i])
            int_current_pid_len = len(list_pid[i])
            int_compare_result_pid_len = len(list_pid_alphabet)
            if int_compare_result_pid_len == int_current_pid_len and int_current_pid_len == 16 or int_current_pid_len == 17:
                pass
            else:
                raise error.equalerror()
        print("\nPID compare result: PASS\n")
        
    def email_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: Contain A-Z, a-z, 0-9, @, +, ., _, !, ?
        ### Parameter:
        ###     actual_result: ["email1", "email2", ...]
        try:
            dic_param = dict(dic_value)
            list_email = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()       
        for i in range(len(list_email)):
            email_pattern = re.compile(r'[A-Za-z0-9@+._!?]')
            list_email_alphabet = re.findall(email_pattern, list_email[i])
            int_current_email_len = len(list_email[i])
            int_compare_result_email_len = len(list_email_alphabet)
            if int_compare_result_email_len == int_current_email_len:
                pass
            else:
                print("\n")
                print(list_email[i])
                print(list_email_alphabet)
                print("\n")
                raise error.equalerror()
        print("\nEmail compare result: PASS\n")
        
    def time_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: time(0-9, -, T, Z, :, ., +)
        ### Parameter:
        ###     actual_result: ["time1", "time2", ...]
        try:
            dic_param = dict(dic_value)
            list_sync_time = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_sync_time)):
            try: 
                sync_time_pattern = re.compile(r'[-TZ:.0-9+]')
                list_sync_time_alphabet = re.findall(sync_time_pattern, list_sync_time[i])
                int_current_sync_time_len = len(list_sync_time[i])
                int_compare_result_sync_time_len = len(list_sync_time_alphabet)
                if int_compare_result_sync_time_len == int_current_sync_time_len:
                    pass
                else:
                    raise error.equalerror()
                         
            except:
                if list_sync_time[i] == None:
                    print("\nThe result is Null\n")
                    pass
                else:
                    raise error.equalerror()
        print("\nTime compare result: PASS\n")

    def null_verify(self, dic_value):
        ### Expected result:
        ###     value: Null
        ### Parameter:
        ###     actual_result:  [[None],[None], ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        print(list_actual_result)
        for i in range(len(list_actual_result)):
            if list_actual_result[i] == None:
                pass
            elif type(list_actual_result[i]) is int:
                pass
            else:
                raise error.equalerror()
        print("\nThe compare result: PASS\n")
        
    def empty_verify(self, dic_value):
        ### Expected result:
        ###     value: Null
        ### Parameter:
        ###     actual_result:  [[],[], ...]
        try:
            dic_param = dict(dic_value)
            list_actual_result = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_actual_result)):
            if len(list_actual_result[i]) == 0:
                pass
            else:
                raise error.equalerror()
        print("\nThe empty list compare result: PASS\n")
        
    def fw_vers_verify(self, dic_value):
        ### Not modify yet(070621)
        ## fw vers. verification
        ## Expected result: 0-9, ., A-Z, a-z-
        ## Parameters:
        ##      - actual_result:
        try:
            dic_param = dict(dic_value)
            list_fw_vers = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        
        for i in range(len(list_fw_vers)):
            fw_vers_pattern = re.compile(r'[0-9A-Za-z.-]')
            list_fw_vers_alphabet = re.findall(fw_vers_pattern, list_fw_vers[i])
            int_current_fw_vers_len = len(list_fw_vers[i])
            int_compare_result_fw_vers_len = len(list_fw_vers_alphabet)
            if int_compare_result_fw_vers_len == int_current_fw_vers_len:
                pass
            else:
                print("\n")
                print(list_fw_vers[i])
                print(list_fw_vers_alphabet)
                print("\n")
                raise error.equalerror()
        print("\nFW Vers. compare result: PASS\n")

    def fw_sku_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: ['Igw-PLUS', 'Cube-X', 'Cube-PLUS', 'Cube-Plus', 'Cube-JUME', 'Cube-JIIS', 'Cube-J1', 'Cube-J', 'Cube-ITANGO', 'Atto-PostF', 'Atto-PLUS']
        ### Parameter:
        ###     actual_result: ["fw_sku1", "fw_sku2", ...]
        try:
            dic_param = dict(dic_value)
            list_fw_sku = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_fw_sku)):
            fw_sku_pattern = re.compile(r'[A-Za-z0-9-_]')
            list_fw_sku_alphabet = re.findall(fw_sku_pattern, list_fw_sku[i])
            int_current_fw_sku_len = len(list_fw_sku[i])
            int_compare_result_fw_sku_len = len(list_fw_sku_alphabet)
            if int_compare_result_fw_sku_len == int_current_fw_sku_len:
                pass
            else:
                raise error.equalerror()
        print("\nFW sku compare result: PASS\n") 
        
    def free_sample_verify(self, dic_value):
        ### Expected result:
        ###     type: string
        ###     value: ["Y", "N", ...]
        ### Parameters:
        ###      - actual_result: ["Y", "N", ...]
        try:
            dic_param = dict(dic_value)
            list_free_sample = eval(dic_param["actual_result"])
        except:
            raise error.equalerror()
        for i in range(len(list_free_sample)):
            if list_free_sample[i] == "Y" or list_free_sample[i] == "N":
                pass
            else:
                raise error.equalerror()
        print("\nFree sample compare result: PASS\n")
        
    def egplus_latest_noti_string_verify(self, dic_value):
        ### Only for API: /api/v1/notifications/events/latests
        ###     
        ### Expected result:
        ###     type: string
        ###     value: Not null
        ### Parameter:
        ###     actual_result: ["string1", "string2", ...]
        dic_param = dict(dic_value)
        list_actual_result = eval(dic_param["actual_result"])
        tuple_cam_value = eval(dic_param["cam_result"])
        if tuple_cam_value[0] is True:
            for i in range(len(list_actual_result)):
                if type(list_actual_result[i]) is str:
                    pass
                else:
                    raise error.equalerror()
            print("\nString compare result: PASS\n")
        elif tuple_cam_value[0] is False:
            pass
        else:
            raise error.notfind()
            
    def egplus_latest_noti_uuid_verify(self, dic_value):
        ### Only for API: /api/v1/notifications/events/latests
        ###     
        ### Expected result:
        ###     type: string
        ###     value: Only contains "-", "a-z", "A-Z", "0-9"
        ###     len: 36
        ### Parameter:
        ###     actual_result: ["uuid1", "uuid2", ...]
        dic_param = dict(dic_value)
        list_actual_result = eval(dic_param["actual_result"])
        tuple_cam_value = eval(dic_param["cam_result"])
        if tuple_cam_value[0] is True:
            for i in range(len(list_actual_result)):
                uuid_pattern = re.compile(r'[0-9a-zA-Z-]')
                list_uuid_alphabet = re.findall(uuid_pattern, list_actual_result[i])
                int_current_uuid_len = len(list_actual_result[i])
                int_compare_result_uuid_len = len(list_uuid_alphabet)
                if int_compare_result_uuid_len == int_current_uuid_len and int_current_uuid_len == 36:
                    pass
                elif int_current_value_len == 0:
                    print("There is a Null vale")
                    pass
                else:
                    raise error.equalerror()
            print("\nUUID compare result: PASS\n")
        elif tuple_cam_value[0] is False:
            pass
        else:
            raise error.notfind()

            
    def api_response_get(self, dic_value):
        ## Due to new class(postman) function: api_result_get
        ## Transfer api response body from list to string
        ##
        ## Required parameters:
        ##  api_result
        ##
        try:
            dic_value['api_result'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            dic_value['api_result'] = eval(dic_value['api_result'])
            str_response_body = str(dic_value['api_result'][1])

            return str_response_body
        except:
            raise error.notfind()            
            
    def environment_set(self, dic_value):
        ## To change cognito token in environment.json file
        ##
        dic_param = dict(dic_value)
        file_name = dic_param["environment_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        print(file_path)
        f = open(file_path, "r+")
        file = f.read()
        f.close()
        dic_file = json.loads(file)
        for i in range(len(dic_file["values"])):
            if dic_file["values"][i]["key"] == "cognito_token":
                dic_file["values"][i]["value"] = dic_param["new_token"]
                break
            else:
                pass
        
        new_file = open(file_path, "w")
        new_file.write(json.dumps(dic_file))
        new_file.close()
        
    def collection_set(self, dic_value):
        ## To change cognito token in collection.json file
        ##
        dic_param = dict(dic_value)
        file_name = dic_param["collection_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)
        target = ""
        target2 = ""
        target3 = ""
        print(file_path)
        f = open(file_path, "r", encoding = "utf-8")
        file = f.read()
        f.close()
        
        dic_file = json.loads(file)
        print(dic_file["item"][0]["name"])
        if dic_file["item"][0]["name"] == dic_param["testcase_name"]:
            target = dic_file["item"][0]["event"][0]["script"]["exec"][12]
            target2 = re.sub(r"^\s+", "", target)
            print(target)
            print("target2")
            print(target2)
        else:
            print("error 1")
        
        if "token" in target2:
            target3 = target2[0:7]
            print("target3")
            print(target3)
        else:
            print("error 2")
        final_target = target3 + "\"" + dic_param["new_token"] + "\","
        dic_file["item"][0]["event"][0]["script"]["exec"][12] = final_target
        print(dic_file)
        json_file = json.dumps(dic_file)
        print("========================================================")
        print(json_file)
        
        file1 = open(file_path, "w")
        file1.write(json_file)
        file1.close()


    def string_verifysame(self, dic_value):
        ## Verify status code from api response
        ## Parameters:
        ##     - api_response
        ##
        dic_param = dict(dic_value)
        #Loading response and transfer to json format:
        str_response = (eval(dic_param["api_response"]))
        print(type(str_response[0]))    
        print(type(dic_param["expected_str"]))

        
        if str(str_response[0]) == dic_param["expected_str"]:
            print("Str: EQUAL")
            pass
        else:
            raise error.equalerror()

    def idtoken_get(self, dic_value):

        dic_param         = dict(dic_value)
        account           = dic_param["username"]
        psd               = dic_param["password"]
        cognito_pool_id   = dic_param["pool_id"]
        cognito_client_id = dic_param["client_id"]
        strAWSRegion      = 'ap-northeast-1'
        strIDToken        = ''

        try:
            client = boto3.client('cognito-idp', region_name=strAWSRegion,
                                  config=botocore.client.Config(signature_version=UNSIGNED))
            objAWS = AWSSRP(
                username=account,
                password=psd,

                ### For EG+ QA ---
                pool_id=cognito_pool_id,
                client_id=cognito_client_id,
                client=client
            )
            dicToken = objAWS.authenticate_user()

            strIDToken = dicToken['AuthenticationResult']['IdToken']
            # print(dicToken)
            print("Cognito token")
            print(strIDToken)
        except Exception as exceptionError:
            # raise error.equalerror()
            print("Exception---->")
            print(exceptionError)
            # raise error.equalerror()
            # raise error.equalerror()
        return strIDToken

    def ndtoken_get(self, dic_value):
        dic_param  = dict(dic_value)
        strIDToken =dic_param["strIDToken"]
        print(strIDToken)
        app_uuid = str(uuid.uuid4())
        # print(app_uuid)
        try:
            strExchange_URL = 'https://api-eg3-qa.nextdrive.io/api/v1/oauth2/tokens/exchange'
            # strExchange_URL = 'https://api-eg3.nextdrive.io/api/v1/oauth2/tokens/exchange'
            dicHeader = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }

            dicBody = {
                'type': 'cognito',
                'token': strIDToken,
                'appUuid': app_uuid
            }
            jsonBody = json.dumps(dicBody)
            objResponse = requests.post(strExchange_URL, data=jsonBody, headers=dicHeader)
            print("appUuid => ".format(app_uuid))
            # print('!!!!!!!!!!!!!!!!!!', objResponse)
            if objResponse.status_code == 200:
                dicResponse = objResponse.json()

                # print('$$$$$$$$$$$$$$$$$$$$$$$')
                # print(strExchange_URL)
                # print(dicHeader)
                # print(jsonBody)
                # print(objResponse)
                # print(dicResponse)
                print("ND token======================>")
                print(dicResponse['accessToken'])
                # print('$$$$$$$$$$$$$$$$$$$$$$$')

                return dicResponse['accessToken']

            else:
                print("!= 200")
                # raise error.equalerror()

        except Exception as exceptionError:
            # raise error.equalerror()
            print("Exception---->")
            print(exceptionError)


    def text_check(self, dic_value):

        dic_param = dict(dic_value)
        apiResult = dic_param["api_result"]
        apiCode   = dic_param["api_code"]
        apiBody   = dic_param["api_body"]

        if apiCode in apiResult:
            print("Found API Code Result : %s" % apiCode)
            pass
        else:
            print("Not Found Target API Response Body")
            raise error.notfind()

        if apiBody in apiResult:
            print("Found API Response Body : %s" % apiBody)
            pass
        else:
            print("Not Found API Response Body")
            raise error.notfind()

    def device_text_check(self, dic_value):

        dic_param = dict(dic_value)
        apiResult = dic_param["api_result"]

        deviceList = ["Cube", "Atto", "Smart Meter", "ECHONET Lite", "Motion Pixi", "Thermo Pixi", "Beep", "Cam", "Modbus", "SmaMe-TypeM", "General BLE"]

        i = 0
        for i in range(len(deviceList)):
            if deviceList[i] in apiResult:
                print("Found device %s" % deviceList[i])
                i += 1
            else:
                print("Not Found device %s" % deviceList[i])
                i += 1
                raise error.notfind()

    def real_string_verifysame(self, dic_value):
        ## Verify status code from api response
        ## Parameters:
        ##     - api_response
        ##
        dic_param = dict(dic_value)
        # Loading response and transfer to json format:
        str_response = dic_param["api_response"]
        print(str_response)
        print(type(dic_param["expected_str"]))

        if str_response == dic_param["expected_str"]:
            print("Str: EQUAL")
            pass
        else:
            raise error.equalerror()























































































    def AAexpected_result_get(self, dic_value):
        ## Get expected result
        ## Parameters:
        ##     - expected_result
        ##
        dic_param = dict(dic_value)
        str_file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "expected_result", dic_param["environment"], dic_param["expected_result"])
        print(str_file_path)
        
        obj_expected_result = open(str_file_path, "r", encoding = 'utf-8')
        str_expected_result = obj_expected_result.read()
        obj_expected_result.close()
        
        uni = str_expected_result.encode("unicode_escape")
        """
        print(uni)
        print(type(uni))
        str_uni = str(uni)
        json_uni = json.dumps(str_uni)
        print(type(json_uni))
        
        
        print("=====")
        print(json_uni)
        print("=====")
        
        list_uni = list(json_uni)
        print(type(list_uni))
        print(list_uni[0])
        
        print("=====")
        jjson_uni = json.loads(json_uni)
        print(type(jjson_uni))
        
        
        remove_json_uni = json_uni.replace("\\\\n", "")
        no_head_tail_string = remove_json_uni[2:-1]
        eval_string = eval(no_head_tail_string)
        
        #print(eval_string)
        print(type(eval_string))
        """
        str_uni2str = str(uni)
        print(str_uni2str)
        print(type(str_uni2str))
        after_string = str_uni2str.replace("\\\\n", "")
        print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        print(after_string)
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        no_head_tail_string = after_string[2:-1]
        print(no_head_tail_string)
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        no_head_tail_string.replace("null", "None")
        json_data = json.loads(no_head_tail_string)
        print("json_data type: below -->")
        print(type(json_data))
        #eval_string = eval(json_data)
        eval_string = json_data
        print(type(eval_string))
        print(eval_string)
        


        return eval_string
        
    def AAread_csv_get(self, dic_value): 
        ## Read csv file and find the target response
        ##
        ## Parameters:
        ##    - csv_filename
        ##    - testcase_name
        ##
        dic_param = dict(dic_value)
        #print("THIS>>>")
        #print(dic_param)
        maxInt = sys.maxsize
         
        while True:
            # decrease the maxInt value by factor 10 
            # as long as the OverflowError occurs.
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt/10)
        
        
        #define csv file:
        str_file_path = os.path.join(os.getcwd(), "ini", "API_NextDrive", "newman_json", dic_param["environment"], "newman",dic_param["csv_filename"])
        list_data = []
        str_target_data = ""
        #open csv file and write into a list:
        with open(str_file_path, newline = "", encoding = "utf-8", errors = 'ignore') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                list_data.append(row)
        #delete first line of the csv:
        del list_data[0]
        """
        print(len(list_data))
        str_list_data = str(list_data)
        print(type(str_list_data))
        print("WWWWWWWWWWWWWWWWWWW")
        uni = str_list_data.encode("unicode_escape")
        str_uni2str = str(uni)
        print(str_uni2str)
        after_string = str_uni2str.replace("\\\\n", "").replace("\\\\r", "")
        print("OOOOOOOOOOOOOOOOOOO")
        print(after_string)
        print(type(after_string))
        print("IIIIIIIIIIIIIIIIIII")
        no_head_tail_string = after_string[2:-1]
        print(no_head_tail_string)
        eval_string = eval(no_head_tail_string)
        print(type(eval_string))
        print("MMMMMMMMMMMMMMMMMMM")
        """
        
        #choose which response data you want:
        for data_no in range(len(list_data)):
            if dic_param["testcase_name"] in list_data[data_no]:
                str_target_data = list_data[data_no]
                #print(str_target_data)
            else:
                pass
        #return response
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        
        print(len(str_target_data))
        uni_list = []
        for i in range(len(str_target_data)):
            #uni_list.append(str_target_data[i].encode("unicode_escape"))
            temp = str_target_data[i].encode("unicode_escape")
            str_temp = str(temp)
            temp2 = str_temp[2:-1]
            #uni_list.append(temp2.replace("\\", ""))
            uni_list.append(temp2)
        print(uni_list)
        final_result = str(uni_list).replace("null", "None")
        print(final_result)
        
    
        
        
        
        
        
        strr_target_data = str(str_target_data)
        uni = strr_target_data.encode("unicode_escape")
        str_uni2str = str(uni)
        print(str_uni2str)
        print(type(str_uni2str))
        after_string = str_uni2str.replace("\\\\n", "")
        print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        print(after_string)
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        no_head_tail_string = after_string[2:-1]
        print(no_head_tail_string)
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        list_2list = no_head_tail_string.replace("\\'", "")
        print(list_2list)
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")


        
        
        
        return final_result
        
    def AAdict_keys_verify(self, dic_value):
        ## Verify dictionary keys
        ## Parameters:
        ##     - expected_result
        ##     - actual_result
        ##
        dic_param = dict(dic_value)
        
        print("ZZZZZZZZZZZZZZZZZZ")
        #dic_except = eval(dic_param["expected_result"])
        #dic_actual = eval(dic_param["actual_result"])
        #print(type(dic_except))
        #print(type(dic_actual))


        str_expected_result = dic_param["expected_result"]
        print(type(str_expected_result))
        list_expected_result = eval(str_expected_result)
        #print(list_expected_result)
        print(type(list_expected_result))
        
        str_actual_result = dic_param["actual_result"]
        print(type(str_actual_result))
        list_actual_result = eval(str_actual_result)
        print(type(list_actual_result))
       
        
        #dic_expected_result = json.loads(dic_param["expected_result"])
        #dic_actual_result = json.loads(dic_param["actual_result"])
        list_expected_keys = list(list_expected_result.keys())
        list_actual_keys = list(list_actual_result.keys())
        print("***********************************************")
        print("***********************************************")
        print("Expected result")
        #print(dic_except)
        print("Actual result")
        #print(dic_actual)
        print("***********************************************")
        print("***********************************************")
        print("***********************************************")
        print("Expected keys")
        print(list_expected_keys)
        print("Actual keys")
        print(list_actual_keys)
        print("***********************************************")
        print("***********************************************")
        for i in range(len(list_expected_keys)):
            if list_expected_keys[i] in list_actual_keys:
                print("Key \"{}\"".format(list_expected_keys[i]).ljust(25) + "exists")
            else:
                print("missing key: ", list_expected_keys[i])
                raise error.equalerror()