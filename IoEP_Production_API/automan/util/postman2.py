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
import imaplib
import email
import re
import time
import datetime

from email.header import decode_header
from datetime import datetime

timeStamp    = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M')
ORG_EMAIL    = "@nextdrive.io"
FROM_EMAIL   = "automan" + ORG_EMAIL
FROM_PWD     = "nngmxdkmkraekcwt"
SMTP_SERVER  = "imap.gmail.com"
SMTP_PORT    = 993
FILTER_EMAIL = "no-reply@nextdrive.io"
WELCOME_EMAIL  = "no-reply@nextdrive.io"

class postman2(object):
    def __init__(self):  
        self.original_path = os.getcwd()
        pass
   
    def command_get(self, dic_value):
        ##  Set postman command
        ##
        ## Required parameters:
        ##      collection      -   Specify a Postman collection as a JSON [file]
        ##      iterations      -   Define the number of iterations to run
        ##      folder          -   Specify a Postman command in collection.

        command = "newman run " + dic_value['collection'] + " --folder " + dic_value['folder']
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

        return command

    def collection_variable_set(self, dic_value):
        ## replace variable in collection.
        ##
        ## Required parameters:    
        ##    json_name      - postman collection with variable
        ##    target_key     - target key
        ##    value          - value to replace
        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)

        f = open(file_path,"r",encoding="utf-8")
        json_file = json.load(f)
        for i in range(len(json_file["variable"])):
            if json_file["variable"][i]["key"] == dic_value["target_key"]:
                json_file["variable"][i]["value"] = dic_value["value"]
                break
            elif i==(len(json_file["variable"])-1):
                print("Can't find target")
                raise error.notfind()
            else:
                pass
        
        f = open(file_path, "w", encoding="utf-8")
        f.write(json.dumps(json_file))
        f.close()

    def collection_variable_get(self, dic_value):
        ## get variable in collection.
        ##
        ## Required parameters:    
        ##    json_name      - postman collection with variable
        ##    target_key     - target key

        file_name = dic_value["json_name"]
        file_path = os.path.join(os.getcwd(), "postman", file_name)

        f = open(file_path,"r",encoding="utf-8")
        json_file = json.load(f)
        result=""
        for i in range(len(json_file["variable"])):
            if json_file["variable"][i]["key"] == dic_value["target_key"]:
                result=json_file["variable"][i]["value"]
                break
            elif i==(len(json_file["variable"])-1):
                print("Can't find target")
                raise error.notfind()
            else:
                pass
        f.close()
        return result

        
    def accesstoken_get(self, dic_value):
        dic_param = dict(dic_value)
        response_body = eval(dic_param["response_result"])
        X = response_body[1]

        try:
            X = re.sub("\Success,", "", X)
        except:
            pass
        print(dic_param["token"])
        X = eval(X)
        Result = X.get("data", {}).get(dic_param["token"])
        print(Result)
        return Result
        
    def delete_gmail_set(self):
        imap = imaplib.IMAP4_SSL(SMTP_SERVER)
        imap.login(FROM_EMAIL, FROM_PWD)
        print("Login gmail [%s] Success\n" % FROM_EMAIL)
        imap.select('inbox')

        type, data   = imap.search(None, 'FROM', FILTER_EMAIL)
        type2, data2 = imap.search(None, 'FROM', WELCOME_EMAIL)

        # Delete access code email ----------------------------
        messages = data[0].split(b' ')
        print(messages)

        for mail in messages:
            _, msg = imap.fetch(mail, "(RFC822)")
            # you can delete the for loop for performance if you have a long list of emails
            # because it is only for printing the SUBJECT of target email to delete
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        # if it's a bytes type, decode to str
                        subject = subject.decode()
            # mark the mail as deleted
            imap.store(mail, "+FLAGS", "\\Deleted")

        # Delete Welcome email ----------------------------
        messages_2 = data2[0].split(b' ')

        for mail_02 in messages_2:
            _, msg_02 = imap.fetch(mail_02, "(RFC822)")
            # you can delete the for loop for performance if you have a long list of emails
            # because it is only for printing the SUBJECT of target email to delete
            for response_02 in msg_02:
                if isinstance(response_02, tuple):
                    msg_02 = email.message_from_bytes(response_02[1])
                    # decode the email subject
                    subject_02 = decode_header(msg_02["Subject"])[0][0]
                    if isinstance(subject_02, bytes):
                        # if it's a bytes type, decode to str
                        subject_02 = subject_02.decode()
            # mark the mail as deleted
            imap.store(mail_02, "+FLAGS", "\\Deleted")
    

    def email_get(self):
        email = ("automan+%s@nextdrive.io" % timeStamp)
        print(email)
        return email