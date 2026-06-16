#coding=utf-8
"""
Created on 2021/09/01
@author     : Dustin Lin
Project     : QAS file result intergration
"""
import automan.tool.error as error
import json
import re
import os
import time
from sqlalchemy.sql.expression import false

class qas_result(object):
    def __init__(self):  
        pass
        
    def qa_list_get(self, valueDict):
        try:
            hFile = open(os.getcwd() + "\\" + valueDict['path'], 'r')
            fileContent = hFile.read() 
            hFile.close()
            
            match = re.findall("([^\r\n]+).qa\n{0,1}", fileContent)
            try:
                match.remove(valueDict["report_file"])
                #match.remove("quick_scan_eis_restore")
            except:
                pass
            print(match)
            return match
        except:
            raise error.nonamevalue()
    
    def xml_list_get(self, valueDict):
        ### Get XML content and return then as a list.
        ###
        ### Required parameters:
        ###     list        - QA file list.
        ###     path_prefix - Log file path prefix.
        ###
        try:
            valueDict['list'] in locals().keys()
            valueDict['path_prefix'] in locals().keys()
            qaList = valueDict['list']
            qaList = eval(qaList)
            qaList = json.dumps(qaList)
            qaList = json.loads(qaList)
        except:
            raise error.nonamevalue()
    
        try:
            resultList = ""
            for item in qaList:
                #print(item)
                filePath = os.getcwd() + "\\log\\" + valueDict['path_prefix'] + item + "\\" + item + ".xml"
                print(filePath)
                try:
                    hFile = open(filePath, 'r')
                    fileContent = hFile.read() 
                    hFile.close()
                    #print(fileContent)
                    xmlName = re.search("\sname=\"([^\r\n\s=\"]+)\"", fileContent)
                    xmlResult = re.search("\sresult=\"(pass|fail)\"", fileContent)
                    print(xmlResult)
                    xmlTime = re.search("\stime=\"([^\r\n\"]+)\"", fileContent)
                    resultList = resultList + "['" + xmlName.group(1) + "', '" + xmlResult.group(1) + "', '" + xmlTime.group(1) + "'];"
                except:
                    print(filePath + " not found.")
                    continue
            resultList = resultList[0:len(resultList) - 1]
            print(resultList)
            return resultList
        except:
            raise error.notfind()
            
    def overall_result_get(self, dict_value):
        """
        * Purpose: Merge all result and make them human readable
        * Parameter:
            - qa_test_result: Result of qa_result_list_get func.
            - environment: Set in QA file
            - project_name: Set in QA file
            - unit: Set in QA file
        
        * Return: 
        * Return type: string
        * Example:
            Auto test finished.
            Environment: environment
            ------------------------------
            Final result(4 APIs): FAIL
            Execution time: 00:03:05
            ------------------------------
            EIS_SANDBOX_POST_auth_login.qa: PASS(00:00:33)
            EIS_GET_health.qa: PASS(00:00:29)
            EIS_GET_accounts.qa: PASS(00:00:54)
            EIS_SANDBOX_POST_auth_refresh-token.qa: FAIL(00:01:09)        
        """
        # Set boolean in qa file: False/True
        if dict_value['only_shows_false'].lower() == 'true':
            ONLY_SHOWS_FALSE = True
        elif dict_value['only_shows_false'].lower() == 'false':
            ONLY_SHOWS_FALSE = False

        str_return_result = ""
        list_qa_result = (dict_value['qa_test_result']).split(';')
        list_marks = [": ", "(", ")"]
        int_total_time = 0
        bool_final_result = True
        len_all_result: int = len(list_qa_result)

        for result in list_qa_result:
            obj_each_time = re.search("'([0-9.]+)( sec){0,1}'", result)
            if obj_each_time:
                int_total_time = int_total_time + float(obj_each_time.group(1))
            else:
                continue

        if ONLY_SHOWS_FALSE:
            for i in range(len_all_result-1, -1, -1):
                temp: list = eval(list_qa_result[i])
                if temp[1].lower() == 'pass':
                    list_qa_result.remove(str(temp))
                else:
                    pass
        else:
            pass

        for result in list_qa_result:
            if len(result) == 0:
                continue

            ## Get boolean result
            obj_each_result = re.search("'(pass|fail)'", result)
            if obj_each_result:
                bool_final_result = (bool_final_result & True) if obj_each_result.group(1) == "pass" else False
            else:
                continue

            ## Get each value
            list_result = re.findall("'([^']+)'", result)
            for i in range(len(list_result)):
                obj_each_time = re.search("([0-9]+).0( sec){0,1}", list_result[i])
                obj_each_result = re.search("(pass|fail)", list_result[i])
                if obj_each_time:
                    str_return_result = str_return_result + time.strftime('%H:%M:%S', time.gmtime(int(obj_each_time.group(1)))) + list_marks[i]
                elif obj_each_result:
                    str_return_result = str_return_result + (list_result[i]).upper() + list_marks[i]
                else:
                    str_return_result = str_return_result + list_result[i] + list_marks[i]
            str_return_result = str_return_result + "\n"

        if ONLY_SHOWS_FALSE is False:
            str_return_result = "------------------------------\n" + str_return_result
        else:
            if len(list_qa_result) == 0:
                pass
            else:
                str_return_result = "-------FAIL Testcase(s)-------\n" + str_return_result

        int_total_time = time.strftime('%H:%M:%S', time.gmtime(int(int_total_time)))
        str_return_result = "Execution time: " + str(int_total_time) + "\n" + str_return_result
        bool_final_result = "PASS" if bool_final_result else "FAIL"
        str_return_result = "Final result({} {}): ".format(len_all_result, dict_value["unit"]) + bool_final_result + "\n" + str_return_result
        #str_return_result = "------------------------------\n" + str_return_result
        str_return_result = "{} test finished.\n".format(dict_value["project_name"], dict_value["environment"]) + str_return_result
        return str_return_result
        
        
        
        
    def final_result_get(self, valueDict):
        ### Merge all result and make them human readable.
        ###
        ### Required parameters:
        ###     text        - Results divide with ";".
        ###         Format: {Result 1};{Result 2};...
        ###         Format(Each result): ['eg_plus_android_ECN_Air_Conditioner', 'pass', '719.0 sec']
        ###     evnironment - QA staging or Production
        ###     project     - IoE, EIS, EG+
        ###     test        - APIs(unit)
        try:
            valueDict['text'] in locals().keys()
        except:
            raise error.nonamevalue()

        resultList = (valueDict['text']).split(";")
        finalResult = True
        for result in resultList:
            if len(result) == 0:
                continue
            eachResult = re.search("'(pass|fail)'", result)
            if eachResult:
                finalResult = (finalResult & True) if eachResult.group(1) == "pass" else False
            else:
                continue
        finalResult = "PASS" if finalResult else "fail"
        print(finalResult)
        return finalResult
    
    