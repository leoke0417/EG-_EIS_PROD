#coding=utf-8
"""
Created on 2021/09/01
@author     : Dustin Lin
Project     : HTTP request
"""
import automan.tool.error as error
import json
import requests, base64

class http_request(object):
    def __init__(self):  
        pass
    
    def HTTP_HEAD_response_get(self, dic_value):
        ##  HTTP request by HEAD method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        request_timeout = 180
        try:
            dic_value['url'] in locals().keys()
            dic_value['header'] in locals().keys()
        except:
            #Key error
            raise error.nonamevalue()
        try:
            http_response = requests.head(dic_value['url'], headers = json.loads(dic_value['header']), timeout = request_timeout)
            status_code = http_response.status_code
            http_response = http_response.json()
            print("HTTP status code: ", status_code)
            print("HTTP response: ", http_response)
            #http_response['statusCode'] = status_code
            return http_response, status_code
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
            
    def HTTP_POST_response_get(self, dic_value):
        ##  HTTP request by POST method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        request_timeout = 180
        try:
            dic_value['url'] in locals().keys()
            dic_value['header'] in locals().keys()
            dic_value['body'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            http_response = requests.post(dic_value['url'], headers = json.loads(dic_value['header']), json = json.loads(dic_value['body']), timeout = request_timeout)
            status_code = http_response.status_code
            http_response = http_response.json()
            print("HTTP status code: ", status_code)
            print("HTTP response: ", http_response)
            #http_response['status_code'] = status_code
            return http_response, status_code

        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
        

        
    def HTTP_PUT_response_get(self, dic_value):
        ##  HTTP request by PUT method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        request_timeout = 180
        try:
            dic_value['url'] in locals().keys()
            dic_value['header'] in locals().keys()
            dic_vlaue['body'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            http_response = requests.put(dic_value['url'], headers = json.loads(dic_value['header']), json = json.loads(dic_value['body']), timeout = request_timeout)
            status_code = http_response.status_code
            http_response = http_response.json()
            print("HTTP status code: ", status_code)
            print("HTTP response: ", http_response)
            #http_response['status_code'] = status_code
            return http_response, status_code
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()    

    def HTTP_DELETE_response_get(self, dic_value):
        ##  HTTP request by DELETE method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        request_timeout = 180
        try:
            dic_value['url'] in locals().keys()
            dic_value['header'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            http_response = requests.delete(dic_value['url'], headers = json.loads(dic_value['header']), timeout = request_timeout)
            status_code = http_response.status_code
            http_response = http_response.json()
            print("HTTP status code: ", status_code)
            print("HTTP response: ", http_response)
            #http_response['status_code'] = status_code
            return http_response, status_code
        except ValueError:
            raise notfind()
        except:
            raise error.onqaserror()  
            
    def HTTP_GET_response_get(self, dic_value):
        ##  HTTP request by GET method.
        ##      HTTP request timeout: 180 seconds.
        ##
        ##  Required parameters:
        ##      url             - APP url
        ##      header          - The header of HTTP request
        ##      body            - HTTP request body
        ##
        ##  Return              :
        ##      HTTP response including status code.
        ##
        request_timeout = 180
        try:
            dic_value['url'] in locals().keys()
            dic_value['header'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        try:
            http_response = requests.get(dic_value['url'], headers = json.loads(dic_value['header']), timeout = request_timeout)
            status_code = http_response.status_code
            http_response = http_response.json()
            print("HTTP status code: ", status_code)
            print("HTTP response: ", http_response)
            #http_response['status_code'] = status_code
            return http_response, status_code
        except ValueError:
            raise error.notfind()
        except:
            raise error.onqaserror()
    

   