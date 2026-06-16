#coding=utf-8
"""
Created on: 2022/03/10

@author: Dustin Lin
"""
"""import os
print(os.path.expanduser('~/.tcms.conf'))"""

from tcms_api import TCMS
import automan.tool.error as error  
import configparser
import datetime
import os
import json
import re
import time

class autokiwi():
    def __init__(self):
        try:
            self.rpc_client = TCMS()
            self.config = configparser.ConfigParser()
            self.config_path = os.path.join(os.getcwd(), "conf", "autokiwi.conf")
            self.config.read(self.config_path, encoding = "utf-8")
            self.str_now_time = datetime.datetime.now()
            self.str_format_time = self.str_now_time.strftime("%Y%m%d_%H%M%S")
            self.int_timeout = 0.3
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()         
        
    def login_set(self):
        try:
            self.rpc_client.exec.Auth.login(self.config.get("Login", "username"), self.config.get("Login", "password"))
            print("Login successfully")
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()
            
    def logout_set(self):
        try:
            self.rpc_client.exec.Auth.logout()
            print("Logout successfully")
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()
            
    def user_id_get(self):
        """
        Not use
        """
        try:
            user_info = self.rpc_client.exec.User.filter()
            user_id = user_info[0]['id']
            print("Current user ID: ", user_id)
            return user_id
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()
            
    def testplan_get(self, dict_value):
        """
        * Purpose: Find the specific testplan
        * Parameter:
            - testplan_id: Set in QA file
            
        * Return: A list of TestPlan information
        * Return type: list(dict)
        * Example:
        [{'id': 423, 'create_date': '2022-02-25 04:07:16', 'extra_link': None, 'is_active': True, 
            'name': 'Autokiwi', 'text': '', 'author_id': 13, 'author': 'Dustin', 'parent_id': None, 
            'parent': None, 'product_id': 57, 'product': 'CEMS Web', 'product_version_id': 106, 
            'product_version': 'unspecified', 'type_id': 20, 'type': 'Performance', 
            'case': [15694, 15695, 16034, 16035], 'tag': [], 'default_product_version': 'unspecified'}]
        """
        try:
            int_testplan_id = int(dict_value["testplan_id"])
            testplan_info = self.rpc_client.exec.TestPlan.filter({'id': int_testplan_id})
            time.sleep(self.int_timeout)
            return testplan_info
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror() 
    
    def testplan_case_id_get(self, dict_value):
        """
        * Purpose: Get the Testcase ID from the testplan information, which got from testplan_get func.
        * Parameter:
            - testplan_info: Result of testplan_get func.
                -> Example: [{'id': 423, 'create_date': '2022-02-25 04:07:16', 'extra_link': None, 'is_active': True, 'name': 'Autokiwi',
                                'text': '', 'author_id': 13, 'author': 'Dustin', 'parent_id': None, 'parent': None, 'product_id': 57, 
                                'product': 'CEMS Web', 'product_version_id': 106, 'product_version': 'unspecified', 'type_id': 20, 
                                'type': 'Performance', 'case': [15694, 15695, 16034, 16035, 16132, 16133, 16134, 16135], 
                                'tag': [], 'default_product_version': 'unspecified'}]
        
        * Return: A list of TestCase ID
        * Return type: list
        * Example:
        [15694, 15695, 16034, 16035, 16132, 16133, 16134, 16135]
        """
        try:
            str_testplan_info = dict_value["testplan_info"]
            list_testplan_info = eval(str_testplan_info)
            list_testcase_id = list_testplan_info[0]['case']
            time.sleep(self.int_timeout)
            return list_testcase_id
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror() 
            
    def testcase_info_get(self, dict_value):
        """
        * Purpose: Get each TestCase information
        * Parameter:
            - testcase_id_list: Result of testcase_info_get func.
                -> Example: [15694, 15695, 16034, 16035, 16132, 16133, 16134, 16135]
                
        * Return: A list of simplified information(id, category, script, is_automated)
            - Note: Raw data
                Example:
                [{'arguments': '', 'id': 16034, 'create_date': '2022-03-11 05:50:13', 'extra_link': None, 
                    'is_automated': True, 'notes': '', 
                    'text': '**Scenario**: ... what behavior will be tested ...\n  **Given** ... conditions ...\n  **When** ... actions ...\n  **Then** ... expected results ...\n\n*Actions*:\n\n1. item\n2. item\n3. item\n\n*Expected results*:\n\n1. item\n2. item\n3. item', 
                    'requirement': None, 'script': 'EIS_SANDBOX_POST_auth_login', 'summary': 'dontgethereEIS_SANDBOX_POST_auth_login', 'author_id': 13, 
                    'author': 'Dustin', 'case_status_id': 2, 'case_status': 'CONFIRMED', 'category_id': 252, 'category': 'RAT', 
                    'default_tester_id': None, 'default_tester': None, 'priority_id': 1, 'priority': 'P1', 'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': []}]
        * Return type: list(tuple)
        * Example:
        [(15694, 'UI', 'EIS_SANDBOX_POST_auth_login', True, 'P1'), (15695, 'UI', 'EIS_GET_health', True, 'P1'), (16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P5'), (16132, 'TOFT', 'EIS_GET_app-labels', True, 'P1'), (16133, 'TOFT', 'EIS_GET_auth_profile', True, 'P1'), (16134, 'FAST', 'EIS_GET_clients', True, 'P2'), (16135, 'FAST', 'EIS_GET_accounts_{id}', True, 'P3')]
        """
        try:
            str_testcase_id = dict_value["testcase_id_list"]
            list_testcase_id = eval(str_testcase_id)
            list_testcase_info = []
            for tc in range(len(list_testcase_id)):
                tc_result = self.rpc_client.exec.TestCase.filter({'id': list_testcase_id[tc]})
                time.sleep(self.int_timeout)
                list_testcase_info.append((tc_result[0]['id'], tc_result[0]['category'], tc_result[0]['script'], tc_result[0]['is_automated'], tc_result[0]['priority']))
            return list_testcase_info
        except Exception as exceptError:
            print("=====> Exception")
            print(exceptError)
            raise error.equalerror()
 
    def testcase_filter_get(self, dict_value):
        """
        * Purpose: To find specific testcase base on category & is_automated column
        * Parameter:
            - testcase_info: Result of testcase_info_get func.
                -> Example: [(15694, 'UI', 'EIS_SANDBOX_POST_auth_login', True, 'P1'), (15695, 'UI', 'EIS_GET_health', True, 'P1'), (16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), 
                            (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P5'), (16132, 'TOFT', 'EIS_GET_app-labels', True, 'P1'), (16133, 'TOFT', 'EIS_GET_auth_profile', True, 'P1'), 
                            (16134, 'FAST', 'EIS_GET_clients', True, 'P2'), (16135, 'FAST', 'EIS_GET_accounts_{id}', True, 'P3')]
            - category: Set in QA file
                -> Parameter: RAT, FAST, TOFT, FET, UI, ALL * combine with ";" (e.g., RAT;FET)
            - is_automated: Set in QA file
                -> Parameter: True, False, ALL
            
        * Return: Find testcases by category & is_automated
        * Return type: list(tuple)
        * Example:
        [(16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P5')]
        """
        list_category = ['RAT', 'FAST', 'TOFT', 'FET', 'UI', 'ALL']
        list_is_automated = ['True', 'False', 'ALL']   
        list_category = dict_value["category"].split(";")
        for category in range(len(list_category)):
            if list_category[category] not in list_category:
                raise error.nonamevalue()
            else:
                pass
        list_testcase_info = eval(dict_value["testcase_info"])
        
        if dict_value['category'] != 'ALL':
            for tc in range(len(list_testcase_info)-1, -1, -1):
                if list_testcase_info[tc][1] not in list_category:
                    list_testcase_info.pop(tc)
                else:
                    pass
        else:
            pass

        if dict_value['is_automated'] == 'True':
            bool_is_automated = True
        elif dict_value['is_automated'] == 'False':
            bool_is_automated = False
        
        if dict_value['is_automated'] != 'ALL':
            for tc in range(len(list_testcase_info)-1, -1, -1):
                if list_testcase_info[tc][3] != bool_is_automated:
                    list_testcase_info.pop(tc)
                else:
                    pass
        else:
            pass
           
        print("Total testcase:", len(list_testcase_info))
        return list_testcase_info
        
    def testcase_sort_get(self, dict_value):
        """
        * Purpost: Get testcase list and sort by priority
        * Parameter:
            - remained_testcase_info: Result of testcase_filter_get func.
                -> Example: [(16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P1')]
            
        * Return: Testcases sorted by priority
        * Return type: list(tuple)
        * Example:
        [(16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P1'), (16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), ]
        """
        list_remained_testcase = eval(dict_value["remained_testcase_info"])
        list_sorted_testcase = []
        list_priority = ['P1', 'P2', 'P3', 'P4', 'P5']
        for pr in range(len(list_priority)):
            for tc in range(len(list_remained_testcase)):
                if list_remained_testcase[tc][4] == list_priority[pr]:
                    list_sorted_testcase.append(list_remained_testcase[tc])
                else:
                    pass
        return list_sorted_testcase
        
    def testrun_create(self, dict_value):
        """
        * Purpose: Create a TestRun, and write TestRun_name, TestRun_id in conf/autokiwi.conf
        * Parameter: 
            - testplan_info: Result of testplan_get func.
                -> Example: [{'id': 423, 'create_date': '2022-02-25 04:07:16', 'extra_link': None, 'is_active': True, 'name': 'Autokiwi',
                                'text': '', 'author_id': 13, 'author': 'Dustin', 'parent_id': None, 'parent': None, 'product_id': 57, 
                                'product': 'CEMS Web', 'product_version_id': 106, 'product_version': 'unspecified', 'type_id': 20, 
                                'type': 'Performance', 'case': [15694, 15695, 16034, 16035, 16132, 16133, 16134, 16135], 
                                'tag': [], 'default_product_version': 'unspecified'}]
        
        * Return: None
        """
        list_testplan_info = eval(dict_value["testplan_info"])
        dict_testplan_info = list_testplan_info[0]
        
        int_manager_id = dict_testplan_info["author_id"]
        int_plan_id = dict_testplan_info["id"]
        
        list_build_info = self.rpc_client.exec.Build.filter({"product_id": dict_testplan_info["product_id"]})
        time.sleep(self.int_timeout)
        int_build_id = list_build_info[0]['id']
        
        str_summary = dict_testplan_info["name"] + "_" + self.str_format_time + "_TestRun"
        
        dict_testrun_param = {
            'build': int_build_id,
            'manager': int_manager_id,
            'plan': int_plan_id,
            'summary': str_summary
        }
        
        testrun_info = self.rpc_client.exec.TestRun.create(dict_testrun_param)
        time.sleep(self.int_timeout)
        self.config.set("TestRun_info", "TestRun_name", testrun_info["summary"])
        self.config.set("TestRun_info", "TestRun_id", str(testrun_info["id"]))
        self.config.write(open(self.config_path, 'w'))
        print(dict_testrun_param)
        print(testrun_info)
        pass
        
    def testrun_case_add(self, dict_value):
        """
        * Purpose: Add a TestCase to the selected TestRun
        * Parameter:
            - remained_testcase: Result of testcase_sort_get func.
                -> Example: [(16132, 'TOFT', 'EIS_GET_app-labels', True, 'P1'), (16133, 'TOFT', 'EIS_GET_auth_profile', True, 'P1'), 
                            (16134, 'FAST', 'EIS_GET_clients', True, 'P2'), (16135, 'FAST', 'EIS_GET_accounts_{id}', True, 'P3'), 
                            (16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P5')]
        
        * Return: None
        """
        list_remained_testcase = eval(dict_value["remained_testcase"])
        int_testrun_id = int(self.config.get("TestRun_info", "TestRun_id"))
        for tc in range(len(list_remained_testcase)):
            self.rpc_client.exec.TestRun.add_case(int_testrun_id, list_remained_testcase[tc][0])
            time.sleep(self.int_timeout)
            
        
    def qas_create(self, dict_value):
        """
        * Purpose: Create a qas file & add testcases to it
        * Parameter:
            - remained_testcase: Result of testcase_sort_get func.
                -> Example: [(16132, 'TOFT', 'EIS_GET_app-labels', True, 'P1'), (16133, 'TOFT', 'EIS_GET_auth_profile', True, 'P1'), 
                            (16134, 'FAST', 'EIS_GET_clients', True, 'P2'), (16135, 'FAST', 'EIS_GET_accounts_{id}', True, 'P3'), 
                            (16034, 'RAT', 'EIS_GET_accounts', True, 'P4'), (16035, 'RAT', 'EIS_SANDBOX_POST_auth_refresh-token', True, 'P5')]
            - testplan_info: Result of testplan_get func.
                -> Example: [{'id': 423, 'create_date': '2022-02-25 04:07:16', 'extra_link': None, 'is_active': True, 'name': 'Autokiwi', 'text': '',
                            'author_id': 13, 'author': 'Dustin', 'parent_id': None, 'parent': None, 'product_id': 57, 'product': 'CEMS Web', 
                            'product_version_id': 106, 'product_version': 'unspecified', 'type_id': 20, 'type': 'Performance', 
                            'case': [15694, 15695, 16034, 16035, 16132, 16133, 16134, 16135], 'tag': [], 'default_product_version': 'unspecified'}]
        
        * Return: None
        """
        list_testplan_info = eval(dict_value["testplan_info"])
        dict_testplan_info = list_testplan_info[0]
        str_qas_filepath = os.path.join(os.getcwd(), "qa", "autokiwi.qas")
        list_remained_testcase = eval(dict_value["remained_testcase"])
        qas_file = open(str_qas_filepath, "w")
        for tc in range(len(list_remained_testcase)):
            qas_file.write(list_remained_testcase[tc][2] + ".qa\n")
        qas_file.close()
        
    def testrun_case_get(self):
        """
        * Purpose: Get TestRun ID from conf/autokiwi.conf & Get each TestCase information in TestRun
        * Parameter:
            - None
        * Return: A list of TestCase information
        * Return type: list(dict)
        * Example:
        [{'arguments': '', 'id': 16034, 'create_date': '2022-03-11 05:50:13', 'extra_link': None, 'is_automated': True, 'notes': '', 
        'text': '**Scenario**: ... what behavior will be tested ...\n  **Given** ... conditions ...\n  **When** ... actions ...\n  **Then** ... expected results ...\n\n*Actions*:\n\n1. item\n2. item\n3. item\n\n*Expected results*:\n\n1. item\n2. item\n3. item', 
        'requirement': None, 'script': 'EIS_SANDBOX_POST_auth_login', 'summary': 'dontgethereEIS_SANDBOX_POST_auth_login', 'author_id': 13, 
        'author': 'Dustin', 'case_status_id': 2, 'case_status': 'CONFIRMED', 'category_id': 252, 'category': 'RAT', 'default_tester_id': None, 
        'default_tester': None, 'priority_id': 1, 'priority': 'P1', 'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 
        'execution_id': 51933, 'status': 'IDLE'}, 
        {'arguments': '', 'id': 16035, 'create_date': '2022-03-11 05:50:38', 'extra_link': None, 'is_automated': True, 'notes': '', 
        'text': '**Scenario**: ... what behavior will be tested ...\n  **Given** ... conditions ...\n  **When** ... actions ...\n  **Then** ... expected results ...\n\n*Actions*:\n\n1. item\n2. item\n3. item\n\n*Expected results*:\n\n1. item\n2. item\n3. item', 
        'requirement': None, 'script': 'EIS_SANDBOX_POST_auth_refresh-token', 'summary': 'dontgethereEIS_SANDBOX_POST_auth_refresh-token', 'author_id': 13, 
        'author': 'Dustin', 'case_status_id': 2, 'case_status': 'CONFIRMED', 'category_id': 252, 'category': 'RAT', 'default_tester_id': None, 
        'default_tester': None, 'priority_id': 1, 'priority': 'P1', 'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 'execution_id': 51934, 'status': 'IDLE'}]
        """
        int_testrun_id = int(self.config.get("TestRun_info", "TestRun_id"))
        list_testrun_case_info = self.rpc_client.exec.TestRun.get_cases(int_testrun_id)
        time.sleep(self.int_timeout)
        return list_testrun_case_info
        
    def testrun_status_get(self, dict_value):
        """
        * Purpose: Get testcase execution_id and test result
        * Parameter:
            - testrun_case_info: Result of testrun_case_get func.
                -> Example: [{'arguments': '', 'id': 15694, 'create_date': '2022-02-25 04:12:27', 'extra_link': None, 'is_automated': True, 'notes': '', 'text': 'Test step', 
                            'requirement': None, 'script': 'EIS_SANDBOX_POST_auth_login', 'summary': 'api_testcase_1 => login', 'author_id': 13, 'author': 'Dustin', 'case_status_id': 2, 
                            'case_status': 'CONFIRMED', 'category_id': 254, 'category': 'UI', 'default_tester_id': None, 'default_tester': None, 'priority_id': 1, 'priority': 'P1', 
                            'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 'execution_id': 52351, 'status': 'PASSED'}, 
                            {'arguments': '', 'id': 15695, 'create_date': '2022-02-25 06:17:01', 'extra_link': None, 'is_automated': True, 'notes': '', 'text': 'Test step', 
                            'requirement': None, 'script': 'EIS_GET_health', 'summary': 'api_testcase_2-Get health', 'author_id': 13, 'author': 'Dustin', 'case_status_id': 2, 
                            'case_status': 'CONFIRMED', 'category_id': 254, 'category': 'UI', 'default_tester_id': None, 'default_tester': None, 'priority_id': 1, 'priority': 'P1',
                            'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 'execution_id': 52352, 'status': 'PASSED'}, 
                            {'arguments': '', 'id': 16034, 'create_date': '2022-03-11 05:50:13', 'extra_link': None, 'is_automated': True, 'notes': '', 'text': 'Test step', 
                            'requirement': None, 'script': 'EIS_GET_accounts', 'summary': 'GET account', 'author_id': 13, 'author': 'Dustin', 'case_status_id': 2, 
                            'case_status': 'CONFIRMED', 'category_id': 252, 'category': 'RAT', 'default_tester_id': None, 'default_tester': None, 'priority_id': 4, 'priority': 'P4', 
                            'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 'execution_id': 52353, 'status': 'PASSED'}, 
                            {'arguments': '', 'id': 16035, 'create_date': '2022-03-11 05:50:38', 'extra_link': None, 'is_automated': True, 'notes': '', 
                            'text': 'Test step', 'requirement': None, 'script': 'EIS_SANDBOX_POST_auth_refresh-token', 'summary': 'dontgethereEIS_SANDBOX_POST_auth_refresh-token', 
                            'author_id': 13, 'author': 'Dustin', 'case_status_id': 2, 'case_status': 'CONFIRMED', 'category_id': 252, 'category': 'RAT', 'default_tester_id': None, 
                            'default_tester': None, 'priority_id': 5, 'priority': 'P5', 'reviewer_id': None, 'reviewer': None, 'plan': [423], 'component': [], 'tag': [], 'execution_id': 52354, 'status': 'FAILED'}]
            - xml_list: Result of xml_list_get func. 
        
        * Return: A list of Test result
        * Return type: list(tuple)
        * Example:
        [(51933, 'pass'), (51934, 'fail')]
        """
        list_testrun_case_info = eval(dict_value["testrun_case_info"])
        str_qas_run_result = dict_value["xml_list"]
        list_temp = str_qas_run_result.split(";")
        list_qas_run_result = []
        for result in range(len(list_temp)):
            list_qas_run_result.append(eval(list_temp[result]))
        list_final_result = []
        if len(list_testrun_case_info) == len(list_qas_run_result):
            for tc in range(len(list_testrun_case_info)):
                int_execution_id = list_testrun_case_info[tc]['execution_id']
                str_tc_name = list_testrun_case_info[tc]['script']
                for result in range(len(list_qas_run_result)):
                    if str_tc_name in list_qas_run_result[result][0]:
                        tuple_result = (int_execution_id, list_qas_run_result[result][1])
                        list_final_result.append(tuple_result)
                    else:
                        pass
        else:
            raise error.equalerror()
        return list_final_result

    def testrun_status_update(self, dict_value):
        """
        * Purpose: Update TestRun result
        * Parameter:
            - execution_result: Result of testrun_status_get func.
            
        * Return: None
        """
        list_final_result = eval(dict_value["execution_result"])
        for result in range(len(list_final_result)):
            if list_final_result[result][1] == 'pass':
                self.rpc_client.exec.TestExecution.update(list_final_result[result][0], {'status':4})
                time.sleep(self.int_timeout)
            elif list_final_result[result][1] == 'fail':
                self.rpc_client.exec.TestExecution.update(list_final_result[result][0], {'status':5})
                time.sleep(self.int_timeout)
            else:
                raise error.equalerror()
                
    def qa_title_list_get(self, dict_value):
        """
        * Purpose: Get each qa test title
        * Parameter:
            - path: Set in QA file(qas file path)
        """
        try: 
            str_file_path = os.path.join(os.getcwd(), dict_value['path'])
            obj_file = open(str_file_path)
            str_file_content = obj_file.read()
            obj_file.close()
            list_match =re.findall("([^\r\n]+).qa\n{0,1}", str_file_content)
            
            return list_match
        except:
            raise error.nonamevalue()

    def qa_result_list_get(self, dict_value):
        """
        * Purpose: Get qa test result 
        * Parameter:
            - qa_title_list: Result of qa_title_list_get func.
                -> Example: ['EIS_SANDBOX_POST_auth_login', 'EIS_GET_health', 'EIS_GET_accounts', 'EIS_SANDBOX_POST_auth_refresh-token']
            - path_prefix: Log file path prefix
            
        * Return: A list of each test result
        * Return type: string
        * Example:
        ['EIS_SANDBOX_POST_auth_login.qa', 'pass', '33.0'];['EIS_GET_health.qa', 'pass', '29.0'];['EIS_GET_accounts.qa', 'pass', '54.0'];['EIS_SANDBOX_POST_auth_refresh-token.qa', 'fail', '69.0']
        """
        str_qa_test_title = dict_value['qa_title_list']
        list_qa_test_title = eval(str_qa_test_title)
        try:
            str_result = ""
            for tr in list_qa_test_title:
                str_file_name = tr + ".xml"
                str_file_path = os.path.join(os.getcwd(), "log", dict_value['path_prefix'], tr, str_file_name)
                print(str_file_path)
                try:
                    obj_file = open(str_file_path, 'r')
                    str_file_content = obj_file.read()
                    obj_file.close()
                    #print(str_file_content)
                    obj_qa_name = re.search("\sname=\"([^\r\n\s=\"]+)\"", str_file_content)
                    obj_execution_result = re.search("\sresult=\"(pass|fail)\"", str_file_content)
                    obj_execution_time = re.search("\stime=\"([^\r\n\"]+)\"", str_file_content)
                    str_result = str_result + "['" + obj_qa_name.group(1) + "', '" + obj_execution_result.group(1) + "', '" + obj_execution_time.group(1) + "'];"
                except:
                    print(str_file_path + " not found.")
                    continue
            str_result = str_result[0:len(str_result) - 1]
            #print(str_result)
            return str_result
        except Exception as exceptError:
            print("=====> Exception: ")
            print(exceptError)
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

        str_return_result = ""
        list_qa_result = (dict_value['qa_test_result']).split(';')
        list_marks = [": ", "(", ")"]
        int_total_time = 0
        bool_final_result = True
        for result in list_qa_result:
            if len(result) == 0:
                continue
        
            ## Get execution time
            obj_each_time = re.search("'([0-9.]+)( sec){0,1}'", result)
            if obj_each_time:
                int_total_time = int_total_time + float(obj_each_time.group(1))
            else:
                continue
            
            ## Get boolean result
            obj_each_result = re.search("'(pass|fail)'", result)
            if obj_each_result:
                bool_final_result = (bool_final_result & True) if obj_each_result.group(1) == "pass" else False
            else:
                continue
            
            ## Get each value
            list_result = re.findall("'([^']+)'", result)
            total_result_no = len(list_qa_result)
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
            
        str_return_result = "------------------------------\n" + str_return_result
        int_total_time = time.strftime('%H:%M:%S', time.gmtime(int(int_total_time)))
        str_return_result = "Execution time: " + str(int_total_time) + "\n" + str_return_result
        bool_final_result = "PASS" if bool_final_result else "FAIL"
        str_return_result = "Final result({} {}): ".format(len(list_qa_result), dict_value["unit"]) + bool_final_result + "\n" + str_return_result
        str_return_result = "------------------------------\n" + str_return_result
        str_return_result = "{} test finished.\nEnvironment: {}\n".format(dict_value["project_name"], dict_value["environment"]) + str_return_result
        print(str_return_result)
        return str_return_result
   