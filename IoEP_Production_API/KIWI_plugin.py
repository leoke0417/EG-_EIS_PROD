'''
Created on 2021年1月29日

@author: automan
'''
import sys,os,time
from junitparser import JUnitXml
from tcms_api import TCMS
#arguments, author, author_id, case_run, case_status, case_status_id, category, category_id, component, create_date, default_tester, default_tester_id, email_settings, extra_link, id, is_automated, notes, plan, priority, priority_id, requirement, reviewer, reviewer_id, script, summary, tag, testcasecomponent, testcaseplan, testcasetag, text">

def setallidel(runid):
    for case in rpc_client.exec.TestRun.get_cases(runid):
        #print(case)    
        if case['is_automated'] == True:
            rpc_client.exec.TestExecution.update(case['execution_id'],{'status':1})
            
def updateqas(runid):
    qasfd = open(os.path.join(os.getcwd() , 'log', 'KIWI_'+runid , 'KIWI_' + runid +'.xml'),'r')
    xml = JUnitXml.fromfile(qasfd)
    time.sleep(1)
    for suite in xml:
        if (str(suite).find('pass') == -1):
            setpass(runid,suite.name)
        if (str(suite).find('fail') == -1):
            setfail(runid,suite.name)
            #setfail(runid,)
            
            
def setpass(runid,script):
        for case in rpc_client.exec.TestRun.get_cases(runid):
            if (case['script'] == script+'.qa'):
                rpc_client.exec.TestExecution.update(case['execution_id'],{'status':4})
    
def setfail(runid,script):
        for case in rpc_client.exec.TestRun.get_cases(runid):
            if (case['script'] == script+'.qa'):
                rpc_client.exec.TestExecution.update(case['execution_id'],{'status':5})
    
def getqas(runid):
        qasfd = open(os.path.join(os.getcwd() , 'qa', 'KIWI' , 'KIWI_' + runid +'.qas'),'w')
        
        for case in rpc_client.exec.TestRun.get_cases(int(runid)):
            if case['is_automated'] == True:
                qasfd.write(case['script'] +'\n')
        
        


if __name__ == '__main__':
    rpc_client = TCMS()
    
    argv = sys.argv[1:]
    runid = argv[0]
    execmd = argv[1]
    
    #for case in rpc_client.exec.TestRun.get_cases(60):
    #     print(case)   
    
    if execmd == 'getqas':
        getqas(runid)
    
    if execmd == 'setallidel':
        setallidel(runid)
    
    if execmd == 'updateqas':
        updateqas(runid)
    
    #===========================================================================
    # for case in rpc_client.exec.TestRun.get_cases(60):
    #     print(case)    
    #     if case['is_automated'] == True:
    #         case['status'] = "PASSED"
    #         case.update()
    #         rpc_client.exec.TestExecution.update(case['execution_id'],{'status':4})
    #===========================================================================
        
        #default_tester
        #print(test_case.update(3013))
        
