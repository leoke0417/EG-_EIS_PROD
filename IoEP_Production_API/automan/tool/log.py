#coding:utf-8
'''
Created on 2010/12/10

@author: panda.huang
'''
import time as time
import automan.tool.error as error
from xml.dom.minidom import Document
import os
import xml.dom.minidom
from xml.dom.minidom import Node

class Log(object):
    '''
    classdocs
    '''


    def __init__(self,qafile,qalist):
        self.result = []
        self.qafile = qafile
        self.qalist = qalist

        dir = os.path.join(os.getcwd() , "log" , str(self.qafile).split('.')[0])
        if len(self.qafile.split('.qa')) == 1:
            print ("Name is xxxx.qa -> not xxxx")
        else:
            try:
                #print("111",dir)
                self.del_folder(dir)
                os.mkdir(dir)
            except:
                #print "mkdir fail!! : " , dir
                pass
        '''
        Constructor
        '''
    def del_folder(self,folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:         
                os.remove(os.path.join(root, name))     
            for name in dirs:         
                os.rmdir(os.path.join(root, name)) 
                
    def del_file(self,filename):
        pass
    
    def create_testcase_xml(self,xml_log):
        
        filename = str(xml_log).split(os.sep)[-1]
        if self.finall_status() == False:
            result = 'fail'
        else:
            result = 'pass'
        runtime = time.mktime(time.strptime(self.result[-1][1],"%m %d %H:%M:%S %Y")) - time.mktime(time.strptime(self.result[0][1],"%m %d %H:%M:%S %Y"))
        doc = Document()
        testcase = doc.createElement("testcase")
        testcase.setAttribute("time", str(runtime))
        testcase.setAttribute("result", result)
        testcase.setAttribute("name", str(filename).replace('.xml', '.qa'))
        doc.appendChild(testcase)
        f = open(xml_log, 'w')
        doc.writexml(f, indent="  ", encoding='UTF-8')
    
    def parse_case_log(self,index):
        
        dir = os.path.join(os.getcwd() , 'log' , str(self.qafile).split('.')[0] , str(str(self.qalist[index]).split(os.sep)[-1]).split('.')[0])
        try:
            os.mkdir(dir)
        except:
            #print "mkdir fail!! : " , dir
            pass
        self.create_testcase_xml(dir + os.sep + str(str(self.qalist[index]).split(os.sep)[-1]).split('.')[0] + '.xml')
            
    def create_hudson_xml(self):
        total_runtime = 0
        total_fail = 0
        total_pass = 0
        testcase_logs = []
        suite_dir = os.path.join(os.getcwd() , 'log' , str(self.qafile).split('.')[0])
        suite_xml = suite_dir + os.sep +str(self.qafile).split('.')[0]+'.xml'
        for xml_file in self.qalist:
            testcase_dir = suite_dir + os.sep + str(str(xml_file).split(os.sep)[-1]).split('.')[0]
            xml_file = str(str(xml_file).split(os.sep)[-1]).split('.')[0]+ '.xml'
            doc = xml.dom.minidom.parse(testcase_dir + os.sep + xml_file)
            for node in doc.getElementsByTagName("testcase"):
                qa_name = node.getAttribute("name")
                qa_result = node.getAttribute("result")
                if str(qa_result).lower() == 'pass':
                    total_pass = total_pass + 1
                elif str(qa_result).lower() == 'fail':
                    total_fail = total_fail + 1                             
                qa_time = node.getAttribute("time")
                total_runtime = total_runtime + float(qa_time)
                testcase_logs = testcase_logs + [(qa_name,qa_result,qa_time)]
            #
        doc = Document()
        testsuite = doc.createElement("testsuite")
        testsuite.setAttribute("tests", str(total_fail+total_pass))
        testsuite.setAttribute("time", str(total_runtime)+' sec')
        testsuite.setAttribute("error", "0")
        testsuite.setAttribute("failures", str(total_fail))
        testsuite.setAttribute("name", str(self.qafile).split('.')[0])
        for item in testcase_logs:
            testcase = doc.createElement("testcase")
            testcase.setAttribute("time", item[2]+' sec')
            testcase.setAttribute("result", item[1])
            testcase.setAttribute("name", str(item[0]).split('.')[0])
            if str(item[1]).lower() == 'fail':
                failure = doc.createElement("failure")
                failure.setAttribute("message", 'This case is FAIL!!')
                testcase.appendChild(failure)
                #<failure message="FAIL !!"/>
            testsuite.appendChild(testcase)  
        
        doc.appendChild(testsuite)
        f = open(suite_xml, 'w')
        doc.writexml(f, indent="  ", encoding='UTF-8')
    

       
    def parse_log(self,result,command):
        print ('Line : ' + str(command[0]) +' ---> '+ ' '.join(command[1:]))
        self.result.append((result,time.strftime("%m %d %H:%M:%S %Y", time.localtime())))
        if result == 0:
            print ("result = PASS")
        else:
            print ("result = FAIL")
            print ("result code = " + str(result))
        print ('Stop : ' + time.ctime() +'\n')

    def finall_status(self):
        status = True
        for index in range(len(self.result)):
            if self.result[index][0] == 1:
                status = False
        return status