'''
Created on Dec 4, 2020

@author: automan
'''
#10 5 10
#threads(number),time(minutes),period(minutes)

import time,sys,random
import threading
import os,requests
import json,time
from datetime import datetime
def job(i,upload_period,running,datanumber):

    cube_pid = '10d07a5e-4632-011a-2830-0006d2xxxxxx'.replace('xxxxxx',str(100002+i))
    cube_uuid = '10d07a5e-4632-011a-2830-0006d2xxxxxx'.replace('xxxxxx',str(100002+i))
    sm_uuid = '98c1cd31-be8c-481c-96f3-a1f78bxxxxxx'.replace('xxxxxx',str(100002+i))
    email = 'axxxxxx@nextdrive.io'.replace('xxxxxx',str(100002+i))
    #print(email)
    
    while running.is_set():
        sle = int(random.random() * upload_period * 60)
        print("Thread %i : sleep %i secs\n" % (i,sle) )
        time.sleep(sle)
        #get token from API
        token = get_token(cube_uuid)
        #print(token)
        json_data = json.dumps(create_data(sm_uuid,datanumber))
        #try send spi to cloud
        upload_data(token,cube_uuid,json_data)
        #no exception : timeourt
        print("Thread %i : remain %i secs\n" % (i,upload_period * 60 - sle) )
        time.sleep(upload_period * 60 - sle)
        
def upload_data(token, cube_uuid , json_data):
    qa_std = "https://device-data-qa.nextdrive.io/v1/devices/records"
    headers = {'Content-Type': 'application/json' , 'nextdrive-uuid' : cube_uuid , 'nextdrive-session' : token}
    r = requests.post(qa_std, data = json_data , headers = headers )
    #r = requests.post(qa_std, json = json_data)
    #print(r.text)

        
def get_token(cube_uuid):
    #open file or .......get by self
    request_header = {'authorization': '4581qalink_nxd^_^7w'}
    response = requests.get(("https://tools-qa.nextdrive.io/qa/v1/session/uuid/xxxx/expiration/4").replace("xxxx",cube_uuid) , headers = request_header)
    ret = response.json()
    return(ret['data']['session'])

def create_data(sm_uuid,datanumber):

    dataarray = []
    
    for i in range(datanumber):
        timestamp = int(datetime.now().timestamp() * 1000) + i * 10
        value = float(format(random.random()*5,'.2f'))    
        rd = {"device_uuid" : sm_uuid , 
                         "data_uuid" : "c4093618-627a-4c99-b190-4845a98c9b1f",
                         "value" : str(value),
                         "raw_value" : "AAAAAAAAAAHuPleEzJ7exdldie",
                         "tags" : "",
                         "generated_time" : timestamp
                         }
        dataarray.append(rd)
    for i in range(datanumber):
        timestamp = int(datetime.now().timestamp() * 1000) + i * 10
        value = float(format(random.random()*5,'.2f'))    
        rd = {"device_uuid" : sm_uuid , 
                         "data_uuid" : "cd405329-4bab-49a6-a4ee-3da4b0dbed1b",
                         "value" : str(value),
                         "raw_value" : "AAAAAAAAAAHuPleEzJ7exdldie",
                         "tags" : "",
                         "generated_time" : timestamp
                         }
        dataarray.append(rd)    
    jsondata =  { "data" : dataarray }      
    #data = json.dumps(jsondata)
    #print(jsondata)
    return jsondata

if __name__ == '__main__':
    running = threading.Event()
    running.set()
    threads = []
    #50000 24X60 10 15
    #50000 -> user
    #24X60 -> one day
    #10 -> upload data once 10 minutes
    #10 -> 10*2 records into db
    argv = sys.argv[1:]
    print("Thread number : "+argv[0],", Test runtime : "+ argv[1]+" minutes" , ", Upload period : " + argv[2]+" minutes", ", records : 2*" + argv[3])
    threadnumber = int(argv[0])
    test_runtime = int(argv[1])
    upload_period = int(argv[2])
    datanumber = int(argv[3])
    
    for i in range(threadnumber):
        threads.append(threading.Thread(target = job, args = (i,upload_period,running,datanumber,)))
        #print("thread : %i star." % i )  
        threads[i].start()

    while (test_runtime > 0):
        print("Remain minutes : %i" % test_runtime )  
        test_runtime = test_runtime - 1
        time.sleep(60)
    
    for i in range(threadnumber):
        running.clear()
    
    print("waiting thread stop.")  
    for i in range(threadnumber):
        print("waiting thread : %i stop" % i )  
        threads[i].join()
      
    print("finish job")