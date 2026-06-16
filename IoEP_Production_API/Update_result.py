'''
Created on Aug 21, 2020

@author: tim
'''

'''
https://{API_SEVER}/api/v1/subset/{subset}/projects/{projectName}/approval/{buildNumber}
{
  "qaComments": the_comments,    
  "qaApproval": "approved"             // {"approved" | "rejected"} 
}
'''
import sys,time,requests
from junitparser import JUnitXml

if __name__ == '__main__':
    argv = sys.argv[1:]
    project = argv[0]
    version = argv[2]
    subset = argv[1]
    logfile = argv[3]
    xml = JUnitXml.fromfile(logfile)
    time.sleep(1)
    res = '{"qaComments": "QA_auto_test_result","qaApproval" : "approved"}'
    for suite in xml:
        if (str(suite).find('pass') == -1):
            res = '{"qaComments": "QA_auto_test_result","qaApproval" : "rejected"}'
    qa_std = "https://frs-api.nextdrive.io/api/v1/subset/"+subset+"/projects/"+project+"/approval/"+version
    #qa_std = "https://frs-api.nextdrive.io/api/v1/subset/ndos2/projects/Cube-Test/approval/4.0.51008"
    print(qa_std)
    json_data = res
    header = {'content-type': 'application/json',
              'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYsImRhdGEiOnsidXNlcm5hbWUiOiJqZW5raW5zIiwiZW1haWwiOiJqZW5raW5zQG5leHRkcml2ZS5pbyIsInJvbGUiOjV9LCJpYXQiOjE1OTk2MTQ4ODEsImF1ZCI6ImRiNWEzODk0LTY5ZTgtNDZiYy1iMDZjLWMzZWY2YTNjZGEyMCIsImlzcyI6Im5leHRkcml2ZS5pbyIsImp0aSI6ImFmZDZlNzkxLTcwNGMtNGViNy1iMDcxLWI5NzBhZTRjZDgzNiJ9.blei-5XAwzMB6KmlfPqPmsstWhExAleaUw9P3kUWmuDW8WJhalPD87W9p6r95PRgjIShU82jtGMugDLmU0H7pcTPMz0nZVLaUwoKJD5KFC55QOZPCjkEv4tvidgurilD-EEQ3EPotGu18p-8v1gu5s_phW7Xj3MFBrR0kv05FeiXvMsBkHdNIDUCcVzDvZsaVnHjM3eSxJB5kUmYYpz9w2DjrPvMqb7nZBAxW_eWn5CfKunBfTKYJHwcMljLcO2FWzZ6o-IPinryTSvtVzdwXWXkIBHtMkL46UkVVjykiLQ_3sxUolfkSLoUbgq0yO8RZoVZVxo1pIxYBcuPlJ3E6w' 
              }
    #{"approved" | "rejected"} 
    print(json_data)
    r = requests.put(qa_std, data = json_data, headers = header )
    print(str(r.content))