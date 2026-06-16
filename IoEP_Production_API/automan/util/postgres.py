#coding=big5
'''
Created on 2022/07/26

@author: Milton Su edited by biran shang
'''
import automan.tool.error as error
import psycopg2
import datetime
import random
from numpy.distutils.fcompiler import none


class postgres(object):
    def __init__(self):
        '''
        '''
    
    def sql_devices_uuid_get(self,value_dict):
        try:
            'gw_id' in locals().keys()
        except:
            raise error.nonamevalue()   
        conn = psycopg2.connect(database='eg3', user="qa_user", password="kGm:A.=#=])6P^6j", host="pgbouncer-qa.nextdrive.io", port="15432")
        
        sql_query1 ="select uuid from devices where gateway_id = "+ value_dict['gw_id'] + " and model !='Camera'"
        print(sql_query1)
        cur = conn.cursor()
        cur.execute(sql_query1)
        obj = [item[0] for item in cur.fetchall()]
        random_obj = random.choice(obj)
        cur.close()
        conn.close()
        return random_obj
             

    def sql_data_uuid_get(self,value_dict):
        try:
            'devices_uuid' in locals().keys()
        except:
            raise error.nonamevalue()
            
               
        conn = psycopg2.connect(database='eg3', user="qa_user", password="kGm:A.=#=])6P^6j", host="pgbouncer-qa.nextdrive.io", port="15432")
        
        sql_query2 ="select DISTINCT data_uuid from device_data where device_uuid = '"+value_dict['devices_uuid']+"' and generated_date = current_date"
        cur = conn.cursor()
        cur.execute(sql_query2)
        obj = [item[0] for item in cur.fetchall()]
        random_obj = random.choice(obj)
        cur.close()
        conn.close()
        return random_obj
    
    
    def sql_data_scope_get(self,value_dict):
        try:
            'data_uuid' in locals().keys()
        except:
            raise error.nonamevalue()
            
               
        conn = psycopg2.connect(database='eg3', user="qa_user", password="kGm:A.=#=])6P^6j", host="pgbouncer-qa.nextdrive.io", port="15432")
        
        sql_query2 ="select DISTINCT scope from device_data_scope where data_uuid = '"+value_dict['data_uuid']+"'"
        cur = conn.cursor()
        cur.execute(sql_query2)
        obj = [item[0] for item in cur.fetchall()]
        random_obj = random.choice(obj)
        cur.close()
        conn.close()
        return random_obj     
                