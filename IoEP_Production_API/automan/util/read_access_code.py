#coding=utf-8
"""
    File:
        read_access_code.py
    Brief:
        Read access code from gmail when new user sign up
    Author:
        Neo
    History:
        2022/04/13 - Initialization version

"""
import automan.tool.error as error
import configparser
import os
import time
import datetime
import imaplib
import email
import re

from datetime import datetime
from automan.tool.verify import Verify
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from email.header import decode_header

ROOT_PATH    = os.path.abspath('.')
timeStamp    = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M')

ORG_EMAIL    = "@nextdrive.io"
FROM_EMAIL   = "automan" + ORG_EMAIL
FROM_PWD     = "nngmxdkmkraekcwt"
SMTP_SERVER  = "imap.gmail.com"
SMTP_PORT    = 993
FILTER_EMAIL = "no-reply@nextdrive.io"
FORGET_MAIL  = "no-reply@nextdrive.io"
WELCOME_EMAIL= "no-reply@nextdrive.io"

class read_access_code(object):

    def _init_(self):
        pass

    def read_from_mail_get(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        print("Login gmail [%s] Success\n" % FROM_EMAIL)
        mail.select('inbox')

        # rv, data = mail.search(None, 'UNSEEN', 'FROM', 'registrar@stockton.edu')
        rv, data = mail.search(None, 'FROM', FILTER_EMAIL)
        # rv, data = mail.search(None, '(SUBJECT "FSCC Acceptance Letter")')

        if rv != 'OK':
            print("No messages found!")
            exit(0)

        mail_ids = data[0]
        print(mail_ids)

        id_list = mail_ids.split()

        for i in reversed(id_list):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    #msg = email.message_from_string(response_part[1].decode('utf-8'))
                    # msg = email.message_from_bytes(response_part[1])
                    #print(msg)
                    #print("\n")

                    regex = re.compile(r' <!-- 123456 -->\\r\\n                      (\d+)')
                    match = regex.search(str(response_part))
                    # print(str(response_part))
                    # print(match.group(1))

                    access_code = match.group(1)
                    print("Find access code : %s \n" % access_code)

                    path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "access_code.txt"
                    code = open(path, 'w')
                    try:
                        code.write(access_code)
                        code.close()
                        return access_code

                    except:
                        raise error.nonamevalue()

    def read_from_forget_mail_get(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        print("Login gmail [%s] Success\n" % FROM_EMAIL)
        mail.select('inbox')

        # rv, data = mail.search(None, 'UNSEEN', 'FROM', 'registrar@stockton.edu')
        rv, data = mail.search(None, 'FROM', FORGET_MAIL)
        # rv, data = mail.search(None, '(SUBJECT "FSCC Acceptance Letter")')

        if rv != 'OK':
            print("No messages found!")
            exit(0)

        mail_ids = data[0]

        id_list = mail_ids.split()

        for i in reversed(id_list):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    #msg = email.message_from_string(response_part[1].decode('utf-8'))
                    # msg = email.message_from_bytes(response_part[1])
                    #print(msg)
                    #print("\n")

                    regex = re.compile(r' <!-- 123456 -->\\r\\n                      (\d+)')
                    match = regex.search(str(response_part))
                    # print(str(response_part))
                    # print(match.group(1))

                    access_code = match.group(1)
                    print("Find access code : %s \n" % access_code)

                    path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "access_code.txt"
                    code = open(path, 'w')
                    try:
                        code.write(access_code)
                        code.close()
                        return access_code

                    except:
                        raise error.nonamevalue()


    def access_code_from_file_get(self):

        path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "access_code.txt"

        f = open(path, 'r')
        code = f.read()
        print(code)
        f.close()

        return code
    
    def access_token_set(self, dic_value):
        dic_param = dict(dic_value)
        response_body = eval(dic_param["response_body_result"])
        print(response_body)
        X = response_body[1]

        try:
            X = re.sub("\Success,","",X)
        except:
            pass

        X = eval(X)
        Result = X.get("data", {}).get("accessToken")

        path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "access_token.txt"
        code = open(path, 'w')

        try:
            code.write(Result)
            code.close()

        except:
            raise error.nonamevalue()
    
    def access_token_from_file_get(self):

        path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "access_token.txt"

        f = open(path, 'r')
        code = f.read()
        print(code)
        f.close()

        return code

    def refresh_token_set(self, dic_value):
        dic_param = dict(dic_value)
        response_body = eval(dic_param["response_body_result"])
        print(response_body)
        X = response_body[1]

        try:
            X = re.sub("\Success,", "", X)
        except:
            pass

        X = eval(X)
        Result = X.get("data", {}).get("refreshToken")

        path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "refresh_token.txt"
        code = open(path, 'w')

        try:
            code.write(Result)
            code.close()

        except:
            raise error.nonamevalue()

    def refresh_token_from_file_get(self):

        path = ROOT_PATH + os.sep + 'automan' + os.sep + 'util' + os.sep + "refresh_token.txt"

        f = open(path, 'r')
        code = f.read()
        print(code)
        f.close()

        return code