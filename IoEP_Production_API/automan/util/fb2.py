#coding=big5
'''
Created on 2018年7月13日

@author: Tim.Huang
'''
import datetime
from fbchat import Client
from fbchat.models import *
from httplib2 import Http
from json import dumps
from docutils.parsers.rst.directives import uri

class Fb2(object):
    def __init__(self):
        '''
        '''

    def fbmessage_send(self, key):
        client = Client(key['user'], key['password'])
        # print('Own id: {}'.format(client.uid))
        now = datetime.datetime.now()
        text = key['message']
        text = text + " at " + now.strftime("%Y-%m-%d %H:%M:%S")
        client.send(Message(text), thread_id=client.uid, thread_type=ThreadType.USER)
        client.logout()

    def googlemessage_send(self, key):

        url = 'https://chat.googleapis.com/v1/spaces/AAAAfHdGUII/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FWHoi6eGb0FW9KxtTg4YDfd-HpHAix1qF68IhqmCdso%3D'
        url_automan = 'https://chat.googleapis.com/v1/spaces/AAAAZGctPm0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=SVetHmFdzfC7D5yF6HdvUXsXJVGyIAcY9TBuAEqSJNg%3D'
        url_api_test = 'https://chat.googleapis.com/v1/spaces/AAAAKivuhTg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=XB3bDXoYHJjcZ_xsUtj9z01Y2n1kfXG_saLuz6tiQNo%3D'
        brianeo = 'https://chat.googleapis.com/v1/spaces/AAAAKivuhTg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=XB3bDXoYHJjcZ_xsUtj9z01Y2n1kfXG_saLuz6tiQNo%3D'
        brianeobpi = 'https://chat.googleapis.com/v1/spaces/AAAAjBzcmk8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=9lZQjBgUBewVvnSXxGmG3PW4r3bt6Mdu1VZ4Jqn79SM'
        autoreportbpi = 'https://chat.googleapis.com/v1/spaces/AAAAZGctPm0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=P8kLAdC_Cp0VpV6paMDYZTCNPGDxjgkW6bz6Q69siWY%3D'
        chunweiapi = 'https://chat.googleapis.com/v1/spaces/AAAAeRzLYoE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=OkBXoRj0gGhXDpiVZllinm5KgkWP_v4K8peQDFljwY8%3D'
        if "FAIL" in key['message']:
            bot_message = {
                'text': key['message'],
                'cards': [
                    {
                        "sections": [
                            {
                                "widgets": [
                                    {
                                        "image": {
                                            "imageUrl": "https://media.giphy.com/media/nrXif9YExO9EI/giphy.gif",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://jenkins.nextdrive.io/"
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        else:
            bot_message = {
                'text': key['message']}

        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = Http()

        http_obj.request(
            uri=brianeobpi,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )