#coding=big5
'''
Created on 2022/07/26

@author: Milton Su edited by Brian Shang
'''
import automan.tool.error as error
import psycopg2
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class cassandra(object):
    def __init__(self):
        '''
        '''
    
    def sql_devices_datas_get(self,value_dict):
        try:
            'devices_uuid' in locals().keys()
            'datas_uuid' in locals().keys()
        except:
            raise error.nonamevalue()
        
        auth_provider = PlainTextAuthProvider(username='nxd_rd', password='crLYiyigljo04uB4om7wre7eHAPh3cicI5p2TRU3')
        cluster=Cluster(["cassandra-qa.nextdrive.io"],port="19042",auth_provider = auth_provider)
        session=cluster.connect()
        session.set_keyspace('dps')
        sql_query="SELECT value FROM datapoints_last where device_uuid='"+value_dict['devices_uuid']+"' and data_uuid='"+value_dict['datas_uuid']+"'"
        rows=session.execute(sql_query)
        for row in rows:
            return row.value
        cluster.shutdown()
            
         