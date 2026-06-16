#coding=utf-8
"""
Created on 2023/03/10
@author     : Brian Shang
Project     : Postman CLI & Automan Integration
"""


"""
Required

Install:

    
"""
import subprocess
import os
import sys
import csv
import json
import automan.tool.error as error
import re

class postmancli(object):
    def __init__(self):  
        self.original_path = os.getcwd()
        pass
    
    def command_get(self, dic_value):

        command = "postman collection run " + dic_value['collection']
        try:
            dic_value['collection'] in locals().keys()
            dic_key = dic_value.keys()
        except:
            raise error.nonamevalue()

        try:
            if "environment" in dic_key:
                command = command + " -e " + dic_value['environment']
                command = command + " --disable-unicode"
        except:
            raise error.nonamevalue()

        print(command)

        try:

            # 執行命令
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 檢查命令是否成功執行
            if result.returncode == 0:
                # 將命令輸出轉換為字串
                output_str = result.stdout.decode('utf-8')
                # 在這裡對輸出進行進一步處理
                print(output_str)
            else:
                output_str = result.stdout.decode('utf-8')
        except:
            raise error.notfind()
        return output_str

    def status_code_verify(self, dic_value):
        dic_value['api_result'] in locals().keys()
        my_string = dic_value['api_result']
        print(my_string)
        pattern = '\\[(\\d{3})'
        matches = re.findall(pattern, my_string)

        if any(num.startswith('4') or num.startswith('5') for num in matches):
            print(matches)
            raise error.equalerror()
        else:
            print(matches)
            pass

    def response_body_get(self, dic_value):
        dic_value['response_body'] in locals().keys()
        dic_value['number'] in locals().keys()
        number = eval(dic_value['number'])
        my_string = dic_value['response_body']
        pattern2 = re.compile(r"Response Body([^}]+\})")
        matches = pattern2.findall(my_string)
        if number <= 0 :
            print('\n\n'+'\n'.join(matches)+'\n\n')
            return matches
        else:
            print('\n\n'+matches[0]+ '\n\n')
            return matches[0]