# -*- coding: UTF-8 -*-
'''
Created on Mar 5, 2021

@author: shawn lin
'''
import os,sys,requests

strImg = 'NXTDRVUPD.BIN'
strURLTemplate = 'https://download.nextdrive.io/%s/%s/%s'

if __name__ == '__main__':
    listArgv = sys.argv[1:]
    strProject = listArgv[0]
    strVersion = listArgv[1]
    #strSubset = listArgv[1]
    strTargetPath = listArgv[2]
    #strProject = 'cube-plus'
    #strVersion = '4.0.16023'
    #strTargetPath = '/Volumes/build/ota-test-data'
    
    strTargetPath = os.path.join(strTargetPath,strProject)
    if not os.path.exists(strTargetPath):
        os.mkdir(strTargetPath)

    strTargetPath = os.path.join(strTargetPath,strVersion)
    if not os.path.exists(strTargetPath):
        os.mkdir(strTargetPath)
    
    strFWImgURL = strURLTemplate % (strProject,strVersion,strImg)
    objGetObject = requests.get(strFWImgURL)

    with open(os.path.join(strTargetPath,strImg), 'wb') as objFile:
        objFile.write(objGetObject.content)
    objFile.close()
    
