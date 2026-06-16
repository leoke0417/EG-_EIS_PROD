import os
import automan.tool.error as error
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from _ast import Return
from wsgiref import headers
import requests
import json


class dms_api():

        def __init__(self):
            try:
                self.config = configparser.ConfigParser()
                self.str_config_path = os.path.join(os.getcwd(), 'conf', 'dms_config.conf')
                self.config.read(self.str_config_path, encoding='utf-8')
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def config_set(self, dict_value):
            self.config.set(dict_value['section'], dict_value['scope'], dict_value['value'])
            self.config.write(open(self.str_config_path, 'w'))

        def dict_dict_value_get(self, dict_value):
            str_response_body = dict_value['response_body']
            dict_response_body = eval(str_response_body)
            list_values = []
            list_values.append(dict_response_body[dict_value['first_key']][dict_value['second_key']])
            return list_values[0]

        def dict_dict_list_value_get(self, dict_value):
            str_response_body = dict_value['response_body']
            dict_response_body = eval(str_response_body)
            list_values = []
            for i in range(len(dict_response_body[dict_value["first_key"]][dict_value["second_key"]])):
                list_values.append(dict_response_body[dict_value["first_key"]][dict_value["second_key"]][i])
            return list_values

        def post_get(self, dict_value):
            try:
                url = dict_value["url"]
                headers = dict_value["header"]
                headers_json = eval(headers)
                data = dict_value["body"]
                data_json = eval(data)
                actually_response = requests.post(url, json=data_json, headers=headers_json)
                return actually_response.status_code, actually_response.json()
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def delete_get(self, dict_value):
            try:
                url = dict_value["url"]
                headers = dict_value["header"]
                headers_json = eval(headers)
                data = dict_value["body"]
                data_json = eval(data)
                actually_response = requests.delete(url, headers=headers_json, json=data_json)
                return actually_response.status_code, actually_response.json()
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def get_get(self, dict_value):
            try:
                url = dict_value["url"]
                headers = dict_value["header"]
                headers_json = eval(headers)
                actually_response = requests.get(url, headers=headers_json)
                return actually_response.status_code, actually_response.json()
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()



        def status_code_get(self, dict_value):
            return eval(dict_value["response"])[0]

        def response_body_get(self, dict_value):
            return eval(dict_value["response"])[1]


        def ums_login_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/user-management/v1/accounts/login"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def ums_login_header_get(self):
            try:
                headers = {"accept": "application/json", "Content-Type": "application/json"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def ums_login_body_get(self, dict_value):
            try:
                str_email = self.config.get("params", dict_value["email"])
                str_password = self.config.get("params", dict_value["password"])
                str_clientId = self.config.get("params", dict_value["clientId"])
                return f"""{{"email": "{str_email}", "password": "{str_password}", "clientId": "{str_clientId}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_registrations_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/device-management/v1/registrations"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_registrations_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_registrations_body_get(self, dict_value):
            try:
                str_pid = self.config.get("params", dict_value["gw_pid"])
                str_hardwareId = self.config.get("params", dict_value["gw_hardwareId"])
                str_name = self.config.get("params", dict_value["gw_name"])
                return f"""{{"pid": "{str_pid}", "hardwareId": "{str_hardwareId}", "name": "{str_name}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_device_protocol = self.config.get("params", dict_value["device_protocol"])
                return f"""{str_end_point}/device-management/v1/associations/protocols/{str_device_protocol}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_ble_body_get(self, dict_value):
            try:
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                str_ble_name = self.config.get("params", dict_value["ble_name"])
                str_ble_model = self.config.get("params", dict_value["ble_model"])
                str_ble_macAddress = self.config.get("params", dict_value["ble_macAddress"])
                return f"""{{"singleDeviceDsn": "{str_gw_dsn}","name": "{str_ble_name}","model": "{str_ble_model}","connectionInfo": {{"macAddress": "{str_ble_macAddress}"}}}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_deregister_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{str_end_point}/device-management/v1/registrations/{str_gw_dsn}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_deregister_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "*/*", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_deregister_body_get(self, dict_value):
            try:
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{{"dsn": "{str_gw_dsn}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_dissociate_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_ble_dsn = self.config.get("params", dict_value["ble_dsn"])
                return f"""{str_end_point}/device-management/v1/associations/{str_ble_dsn}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_dissociate_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "*/*", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_dissociate_body_get(self, dict_value):
            try:
                str_ble_dsn = self.config.get("params", dict_value["ble_dsn"])
                return f"""{{"dsn": "{str_ble_dsn}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_device_dsn_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_device_dsn = self.config.get("params", dict_value["device_dsn"])
                return f"""{str_end_point}/device-management/v1/devices/{str_device_dsn}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_device_dsn_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_ble_list_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{str_end_point}/device-management/v1/devices/{str_gw_dsn}/ble-list"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_ble_list_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_echonet_list_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{str_end_point}/device-management/v1/devices/{str_gw_dsn}/echonet-list"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_echonet_list_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_topology_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_device_dsn = self.config.get("params", dict_value["device_dsn"])
                return f"""{str_end_point}/device-management/v1/devices/{str_device_dsn}/topology"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_topology_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_wifi_list_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{str_end_point}/device-management/v1/devices/{str_gw_dsn}/wifi-list"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_dsn_wifi_list_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_page_user_uuid_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_page = self.config.get("params", dict_value["page"])
                str_user_uuid = self.config.get("params", dict_value["user_uuid"])
                return f"""{str_end_point}/device-management/v1/devices/?page={str_page}&userUuid={str_user_uuid}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_page_user_uuid_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def css_v1_connection_status_dsn_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_dsn = self.config.get("params", dict_value["gw_dsn"])
                return f"""{str_end_point}/css/v1/connection-status?dsn={str_gw_dsn}"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def css_v1_connection_status_dsn_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()






