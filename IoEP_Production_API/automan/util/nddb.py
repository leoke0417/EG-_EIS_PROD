# -*- coding: UTF-8 -*-
'''
Created on Oct 8, 2021

@author: shawn
'''
import psycopg2

class nddb(object):
    '''
    The class to access ND DB
    '''
    def __init__(self,dicDB):
        self._conn2db(dicDB['strDB'],dicDB['strHost'],dicDB['strPort'],dicDB['strUser'],dicDB['strPW'])
        
        
    def _conn2db(self,strDB,strURL,strPort,strID,strPW):
        try:
            self.objConn = psycopg2.connect(user=strID,
                                            password=strPW,
                                            host=strURL,
                                            port=strPort,
                                            database=strDB)
            self.objCursor = self.objConn.cursor()
            print('NDDB is connected!')
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to NDDB!", error)
        finally:
            print()
        
    
    def query(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            return self.objCursor.fetchall() # list
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying!", error)
            self.objCursor.close()
            self.objConn.close()
        
    
    def update(self,strSQLCmd):
        try:
            self.objCursor.execute(strSQLCmd)
            self.objConn.commit()
            print("Total number of rows updated :", self.objCursor.rowcount)
            print('DB update successfully...')
            print()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while updating!", error)
            self.objCursor.close()
            self.objConn.close()

    def insert(self,strSQLCmd,listData):
        try:
            self.objCursor.execute(strSQLCmd,listData)
            self.objConn.commit()
            print("Total number of rows inserted :", self.objCursor.rowcount)
            print('DB insert successfully...')
            print()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting!", error)
            self.objCursor.close()
            self.objConn.close()

    
    def bulk_insert(self,strSQLCmd,listData):
        try:
            self.objCursor.executemany(strSQLCmd,listData)
            self.objConn.commit()
            print("Total number of rows inserted :", self.objCursor.rowcount)
            print('DB insert successfully...')
            print()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting!", error)
            self.objCursor.close()
            self.objConn.close()
        
        
        
    def closeDB(self):
        self.objCursor.close()
        self.objConn.close()
        print("NDDB connection is closed!")
        
    