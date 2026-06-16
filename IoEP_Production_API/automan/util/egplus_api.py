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


class egplus_api():

        def __init__(self):
            try:
                self.config = configparser.ConfigParser()
                self.str_config_path = os.path.join(os.getcwd(), 'conf', 'egplus_config.conf')
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
                return f"""{str_end_point}/user-management/v1/accounts/app/login"""

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
                str_appUuid = self.config.get("params", dict_value["appUuid"])
                return f"""{{"email": "{str_email}", "password": "{str_password}", "clientId": "{str_clientId}", "appUuid": "{str_appUuid}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_associations_gateways_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/associations/gateways"""

            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_gateways_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_gateways_body_get(self, dict_value):
            try:
                str_pid = self.config.get("params", dict_value["gw_pid"])
                str_hardwareId = self.config.get("params", dict_value["gw_hardwareId"])
                str_name = self.config.get("params", dict_value["gw_name"])
                return f"""{{"pid": "{str_pid}", "profileId": "{str_hardwareId}", "name": "{str_name}"}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_associations_devices_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/associations/devices"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_devices_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_associations_devices_body_get(self, dict_value):
            try:
                str_gw_uuid = self.config.get("params", dict_value["gw_uuid"])
                str_ble_name = self.config.get("params", dict_value["ble_name"])
                str_ble_model = self.config.get("params", dict_value["ble_model"])
                str_ble_service = self.config.get("params", dict_value["ble_service"])
                str_ble_macAddress = self.config.get("params", dict_value["ble_macAddress"])
                return f"""{{"gatewayUuid": "{str_gw_uuid}","name": "{str_ble_name}","model": "{str_ble_model}","service": "{str_ble_service}","attributes": {{"macAddress": "{str_ble_macAddress}"}}}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_devices_deviceUuid_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_ble_uuid = self.config.get("params", dict_value["ble_uuid"])
                return f"""{str_end_point}/api/v1/devices/{str_ble_uuid}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_devices_deviceUuid_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_devices_deviceUuid_dashboard_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_ble_uuid = self.config.get("params", dict_value["ble_uuid"])
                return f"""{str_end_point}/api/v1/devices/{str_ble_uuid}/dashboard"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_devices_deviceUuid_dashboard_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_gateways_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/gateways"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_gateways_gatewayUuid_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_uuid = self.config.get("params", dict_value["gw_uuid"])
                return f"""{str_end_point}/api/v1/gateways/{str_gw_uuid}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_gatewayUuid_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_dissociate_devices_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_ble_uuid = self.config.get("params", dict_value["ble_uuid"])
                return f"""{str_end_point}/api/v1/associations/devices/{str_ble_uuid}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_dissociate_devices_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_dissociate_devices_body_get(self):
            try:
                return f"""{{}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_deregister_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_uuid = self.config.get("params", dict_value["gw_uuid"])
                return f"""{str_end_point}/api/v1/associations/gateways/{str_gw_uuid}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_deregister_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_deregister_body_get(self):
            try:
                return f"""{{}}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_aircon_brands_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/aircon/brands"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_aircon_brands_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_aircon_brands_brandId_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_aircon_brandId = self.config.get("params", dict_value["aircon_brandId"])
                return f"""{str_end_point}/api/v1/aircon/brands/{str_aircon_brandId}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_aircon_brands_brandId_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_posts_latests_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_postnextStartTime = self.config.get("params", dict_value["postnextStartTime"])
                return f"""{str_end_point}/api/v1/posts/latests?nextStartTime={str_postnextStartTime}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_posts_latests_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_app_modbusbrands_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/app/modbus-brands"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_app_modbusbrands_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_app_modbusbrands_brandId_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_modbus_brandId = self.config.get("params", dict_value["modbus_brandId"])
                return f"""{str_end_point}/api/v1/app/modbus-brands/{str_modbus_brandId}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_app_modbusbrands_brandId_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_app_bleBrands_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                return f"""{str_end_point}/api/v1/app/bleBrands"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_app_bleBrands_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_app_bleBrands_brandId_model_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_ble_brandId = self.config.get("params", dict_value["ble_brandId"])
                return f"""{str_end_point}/api/v1/app/bleBrands/{str_ble_brandId}/model"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_app_bleBrands_brandId_model_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_gateways_gatewayUuid_weathers_today_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_uuid = self.config.get("params", dict_value["online_gw_uuid"])
                return f"""{str_end_point}/api/v1/gateways/{str_gw_uuid}/weathers/today"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_gatewayUuid_weathers_today_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()


        def v1_gateways_gatewayUuid_locations_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_uuid = self.config.get("params", dict_value["online_gw_uuid"])
                str_postalCode = self.config.get("params", dict_value["postalCode"])
                return f"""{str_end_point}/api/v1/gateways/{str_gw_uuid}/locations?postalCode={str_postalCode}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_gatewayUuid_locations_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_gatewayUuid_firmwares_latests_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_gw_uuid = self.config.get("params", dict_value["online_gw_uuid"])
                return f"""{str_end_point}/api/v1/gateways/{str_gw_uuid}/firmwares/latests"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_gateways_gatewayUuid_firmwares_latests_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_posts_search_url_get(self, dict_value):
            try:
                str_end_point = self.config.get("end_point", dict_value["environment"])
                str_postkeyword = self.config.get("params", dict_value["postkeyword"])
                return f"""{str_end_point}/api/v1/posts/search?keyword={str_postkeyword}"""
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()

        def v1_posts_search_header_get(self, dict_value):
            try:
                str_token = self.config.get("params", dict_value["token"])
                headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {str_token}"}
                return headers
            except Exception as exceptError:
                print("=====> Exception: ")
                print(exceptError)
                raise error.equalerror()