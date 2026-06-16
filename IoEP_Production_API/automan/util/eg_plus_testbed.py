#coding=utf-8
"""
Created on 2021/02/03
@author     : Roger Wei
Project     : Ecogenie+ APP
"""
import automan.tool.error as error
import os.path, re, time, json, subprocess, configparser, datetime
import xml.etree.ElementTree as ET
from os import listdir
from automan.tool.verify import Verify
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'conf', "eg_plus_testbed.conf"), encoding="utf-8")

def gateway_offline(gateway, timeout):
    ##  Required parameters:
    ##      gateway         - Gateway name
    ##      timeout         - Timeout (In unit of seconds)
    ##
    ##  Expected result:
    ##      Gateway not found in devices list.
    ##
    try:
        print("Wait gateway offline...")
        deviceNotFound = False
        timeInterval = 3
        retry = int(timeout) / timeInterval
        for i in range(int(retry)):
            # Get ADB devices list
            devicesList = ""
            out = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                devicesList += line.decode("big5", "ignore")
            #print("devicesList: \n" + devicesList)
            
            # 'devicesList' sample: 
            #   List of devices attached
            #   CubeI-723403    device
            #   CubeI-72a871    device
            result = re.search("(" + gateway + ")[:\d]*[\t\s]+device", devicesList)
            if not result:
                deviceNotFound = True
                break
            else:
                subprocess.Popen("adb connect " + gateway, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                time.sleep(timeInterval) 
        
        if deviceNotFound:
            print(gateway, " is offline")
        else:
            print(gateway, " is not offline after ", timeout, " seconds")
            raise error.nonamevalue()
    except:
        raise error.nonamevalue()
     
def gateway_online(gateway, timeout):
    ##  Required parameters:
    ##      gateway         - Gateway name
    ##      timeout         - Timeout (In unit of seconds)
    ##
    ##  Expected result:
    ##      Gateway found in devices list.
    ##
    try:
        print("Wait gateway online...")
        deviceFound = False
        timeInterval = 3
        retry = int(timeout) / timeInterval
        for i in range(int(retry)):
            # Get ADB devices list
            devicesList = ""
            out = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                devicesList += line.decode("big5", "ignore")
            #print("devicesList: \n" + devicesList)
            
            # 'devicesList' sample: 
            #   List of devices attached
            #   CubeI-723403    device
            #   CubeI-72a871    device
            result = re.search("(" + gateway + ")[:\d]*[\t\s]+device", devicesList)
            if result:
                deviceFound = True
                break
            else:
                subprocess.Popen("adb connect " + gateway, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                time.sleep(timeInterval) 
        
        if deviceFound:
            print(gateway, " is online")
        else:
            print(gateway, " is not online after ", timeout, " seconds")
            raise error.nonamevalue()
    except:
        raise error.nonamevalue()

def CMD_response(command):
    ### Get CMD response with multiply lines.
    ###
    ### Required parameters:
    ###     command        - CMD command.
    ###
    try:
        response = ""
        out = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in out.stdout:
            line = line.rstrip()
            response += line.decode("big5", "ignore")
        print(response)
        return response
    except:
        raise error.nonamevalue()

def CMD_response_continuously(command, prompt, timeout):
    ### Get CMD response with multiply lines.
    ### Execute command until prompt found or timeout.
    ###
    ### Required parameters:
    ###     command         - CMD command.
    ###     prompt          - Exit condition.
    ###     timeout         - Timeout (In unit of seconds).
    ###
    try:
        response = ""
        execTime = 0
        timeInterval = 1
        timeout = int(timeout)
        out = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        for line in out.stdout:
            line = line.rstrip()
            tempLine = line.decode("big5", "ignore")
            #print(line.decode("big5", "ignore"))
            print(tempLine)
            response += tempLine
            if re.search(prompt, tempLine):
                print("Found prompt")
                break
            elif execTime >= timeout:
                print("Timeout")
                break
            execTime += timeInterval
            #print(execTime)
            time.sleep(timeInterval)
            
        return response
    except:
        raise error.nonamevalue()

def stringToList(inputString):
    inputString = (inputString)[1:len(inputString)]
    inputString = (inputString)[0:len(inputString) - 1]
    inputString = (inputString).replace("'", "")
    inputString = (inputString).replace(", ", ",")
    inputString = (inputString).split(",")
    outputList = list(inputString)
    return outputList

def file_content(path):
    try:
        hFile = open(path, 'r', encoding='utf8', errors='ignore')
        fileContent = hFile.read() 
        hFile.close()
        #print("File content:\n", fileContent)
        return fileContent
    except:
        raise error.nonamevalue()

def text_search(text, regex):
    try:
        fileContent = None
        #fileContent = re.findall("[^\r\n]+" + valueDict['regex'] + "", valueDict['text'])
        fileContent = re.findall(regex, text)
        #print("Text search:\n", fileContent)
        return fileContent
    except:
        raise error.nonamevalue()

class eg_plus_testbed(object):
    
    def _init_(self):
        pass
            
    def qa_list_get(self, valueDict):
        try:
            hFile = open(os.getcwd() + "\\" + valueDict['path'], 'r')
            fileContent = hFile.read() 
            hFile.close()
            
            match = re.findall("([^\r\n]+).qa\n{0,1}", fileContent)
            try:
                match.remove("eg_plus_upload_result")
            except:
                pass
            return match
        except:
            raise error.nonamevalue()
            
    def xml_list_get(self, valueDict):
        ### Get XML content and return then as a list.
        ###
        ### Required parameters:
        ###     list        - QA file list.
        ###     path_prefix - Log file path prefix.
        ###
        try:
            valueDict['list'] in locals().keys()
            valueDict['path_prefix'] in locals().keys()
            qaList = valueDict['list']
            qaList = eval(qaList)
            qaList = json.dumps(qaList)
            qaList = json.loads(qaList)
        except:
            raise error.nonamevalue()

        try:
            resultList = ""
            for item in qaList:
                #print(item)
                filePath = os.getcwd() + "\\log\\" + valueDict['path_prefix'] + item + "\\" + item + ".xml"
                #print(filePath)
                try:
                    hFile = open(filePath, 'r')
                    fileContent = hFile.read() 
                    hFile.close()
                    #print(fileContent)
                    xmlName = re.search("\sname=\"([^\r\n\s=\"]+)\"", fileContent)
                    xmlResult = re.search("\sresult=\"(pass|fail)\"", fileContent)
                    xmlTime = re.search("\stime=\"([^\r\n\"]+)\"", fileContent)
                    resultList = resultList + "['" + xmlName.group(1) + "', '" + xmlResult.group(1) + "', '" + xmlTime.group(1) + "'];"
                except:
                    print(filePath + " not found.")
                    continue
            resultList = resultList[0:len(resultList) - 1]
            print(resultList)
            return resultList
        except:
            raise error.notfind()

    def CMD_response_get(self, valueDict):
        ### Get CMD response with multiply lines.
        ###
        ### Required parameters:
        ###     command        - CMD command.
        ###
        try:
            response = ""
            out = subprocess.Popen(valueDict['command'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                response += line.decode("big5", "ignore")
            print(response)
            return response
        except:
            raise error.nonamevalue()
        
    def CMD_sed_response_get(self, valueDict):
        ### Get CMD response with multiply lines.
        ###
        ### Required parameters:
        ###     command        - CMD command.
        ###
        print("Command: \n", valueDict['command'])
        valueDict['command'] = (valueDict['command']).replace("\\", "\\\\")
        valueDict['command'] = (valueDict['command']).replace("!ba", "$!ba")
        
        print("Command: \n", valueDict['command'])
        try:
            response = ""
            out = subprocess.Popen(valueDict['command'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                response += line.decode("big5", "ignore")
            print(response)
            return response
        except:
            raise error.nonamevalue()
         
    def CMD_response_continuously_get(self, valueDict):
        ### Get CMD response with multiply lines.
        ### Execute command until prompt found or timeout.
        ###
        ### Required parameters:
        ###     command         - CMD command.
        ###     prompt          - Exit condition.
        ###     timeout         - Timeout (In unit of seconds).
        ###
        try:
            response = ""
            execTime = 0
            timeInterval = 1
            timeout = int(valueDict['timeout'])
            out = subprocess.Popen(valueDict['command'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            for line in out.stdout:
                line = line.rstrip()
                tempLine = line.decode("big5", "ignore")
                #print(line.decode("big5", "ignore"))
                print(tempLine)
                response += tempLine
                if re.search(valueDict['prompt'], tempLine):
                    print("Found prompt")
                    break
                elif execTime >= timeout:
                    print("Timeout")
                    break
                execTime += timeInterval
                #print(execTime)
                time.sleep(timeInterval)
                
            return response
        except:
            raise error.nonamevalue()
              
    def INI_value_get(self, valueDict):
        ### Get value from INI file.
        ###
        ### Required parameters:
        ###     ini         - INI file path and name.
        ###     scope       - Scope of value.
        ###
        try:
            print(os.getcwd() + "\\" + valueDict['ini'])
            hFile = open(os.getcwd() + "\\" + valueDict['ini'], 'r')
            file_content = hFile.read()
            hFile.close()
            value = re.search(valueDict['scope'] + "=([^\r\n]+)", file_content)
            value = "" if not value else value.group(1)
            print(value)
            return value
        except:
            raise error.nonamevalue()
        
    def app_version_get(self, valueDict):
        ### Get APP version.
        ###
        ### Required parameters:
        ###     command        - CMD command.
        ###
        try:
            response = ""
            out = subprocess.Popen(valueDict['command'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                response += line.decode("big5", "ignore")
                
            print("Source data: " + response)
            response = re.search("versionName=([^\r\n]+)", response)
            response = "" if not response else response.group(1)
            print("Regexp data: " + response)
            return response
        except:
            raise error.nonamevalue()

    def overall_result_get(self, valueDict):
        ### Merge all result and make them human readable.
        ###
        ### Required parameters:
        ###     text        - Results divide with ";".
        ###         Format: {Result 1};{Result 2};...
        ###         Format(Each result): ['eg_plus_android_ECN_Air_Conditioner', 'pass', '719.0 sec']
        ###     fw_version  - Firmware version.
        ###     app_version - APP version.
        ###
        try:
            valueDict['text'] in locals().keys()
            valueDict['fw_version'] in locals().keys()
            valueDict['app_version'] in locals().keys()
            valueDict['testing_environment'] in locals().keys()
            fwVersion = re.search("\[ro.build.version.release\]: \[([^\r\n]+)\]", valueDict['fw_version'])
            fwVersion = valueDict['fw_version'] if not fwVersion else fwVersion.group(1)
            appVersion = valueDict['app_version']
            testingEnvironment = "QA Staging" if valueDict['testing_environment'] == "qa" else "Not defined"
            testingEnvironment = "Production" if valueDict['testing_environment'] == "production" else testingEnvironment
        except:
            raise error.nonamevalue()
        
        try:
            returnText = ""
            resultList = (valueDict['text']).split(";")
            marksList = [": ", "(", ")"]
            totalTime = 0
            finalResult = True
            for result in resultList:
                if len(result) == 0:
                    continue
            
                ## Get execution time
                eachTime = re.search("'([0-9.]+)( sec){0,1}'", result)
                if eachTime:
                    totalTime = totalTime + float(eachTime.group(1))
                else:
                    continue
                
                ## Get boolean result
                eachResult = re.search("'(pass|fail)'", result)
                if eachResult:
                    finalResult = (finalResult & True) if eachResult.group(1) == "pass" else False
                else:
                    continue
                
                ## Get each value
                result = re.findall("'([^']+)'", result)
                for i in range(len(result)):
                    eachTime = re.search("([0-9]+).0( sec){0,1}", result[i])
                    eachResult = re.search("(pass|fail)", result[i])
                    if eachTime:
                        returnText = returnText + time.strftime('%H:%M:%S', time.gmtime(int(eachTime.group(1)))) + marksList[i]
                    elif eachResult:
                        returnText = returnText + (result[i]).upper() + marksList[i]
                    else:
                        returnText = returnText + result[i] + marksList[i]
                returnText = returnText + "\n"
        
            returnText = "--------------------------------------------------\n" + returnText
            totalTime = time.strftime('%H:%M:%S', time.gmtime(int(totalTime)))
            returnText = "Execution time: " + str(totalTime) + "\n" + returnText
            finalResult = "PASS" if finalResult else "FAIL"
            returnText = "Final result: " + finalResult + "\n" + returnText
            returnText = "--------------------------------------------------\n" + returnText
            returnText = "Application version: " + appVersion + "\n" + returnText
            returnText = "Firmware version: " + fwVersion + "\n" + returnText
            returnText = "--------------------------------------------------\n" + returnText
            returnText = "Testing environment: " + testingEnvironment + "\n" + returnText
            returnText = "Ecogenie+ Quick-Scan test finished.\n" + returnText
            print(returnText)
            return returnText
        except:
            raise error.notfind()

    def gateway_offline_verify(self, valueDict):
        ##  Required parameters:
        ##      gateway         - Gateway name
        ##      timeout         - Timeout (In unit of seconds)
        ##
        ##  Expected result:
        ##      Gateway not found in devices list.
        ##
        try:
            valueDict['gateway'] in locals().keys()
            valueDict['timeout'] in locals().keys()
        except:
            #KeyError
            raise error.nonamevalue()

        print("Gateway offline verifying...")
        deviceNotFound = False
        timeInterval = 3
        retry = int(valueDict['timeout']) / timeInterval
        for i in range(int(retry)):
            # Get ADB devices list
            devicesList = ""
            out = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                devicesList += line.decode("big5", "ignore")
            #print("devicesList: \n" + devicesList)
            
            # 'devicesList' sample: 
            #   List of devices attached
            #   CubeI-723403    device
            #   CubeI-72a871    device
            result = re.search("(" + valueDict['gateway'] + ")[:\d]*[\t\s]+device", devicesList)
            if not result:
                deviceNotFound = True
                break
            else:
                subprocess.Popen("adb connect " + valueDict['gateway'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                time.sleep(timeInterval) 

        if deviceNotFound:
            print(valueDict['gateway'], " is offline")
            pass
        else:
            print(valueDict['gateway'], " is not offline after ", valueDict['timeout'], " seconds")
            
    def gateway_online_verify(self, valueDict):
        ##  Required parameters:
        ##      gateway         - Gateway name
        ##      timeout         - Timeout (In unit of seconds)
        ##
        ##  Expected result:
        ##      Gateway found in devices list.
        ##
        try:
            valueDict['gateway'] in locals().keys()
            valueDict['timeout'] in locals().keys()
        except:
            #KeyError
            raise error.nonamevalue()

        print("Gateway online verifying...")
        deviceFound = False
        timeInterval = 3
        retry = int(valueDict['timeout']) / timeInterval
        for i in range(int(retry)):
            # Get ADB devices list
            devicesList = ""
            out = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in out.stdout:
                line = line.rstrip()
                devicesList += line.decode("big5", "ignore")
            #print("devicesList: \n" + devicesList)
            
            # 'devicesList' sample: 
            #   List of devices attached
            #   CubeI-723403    device
            #   CubeI-72a871    device
            result = re.search("(" + valueDict['gateway'] + ")[:\d]*[\t\s]+device", devicesList)
            if result:
                deviceFound = True
                break
            else:
                subprocess.Popen("adb connect " + valueDict['gateway'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                time.sleep(timeInterval) 

        if deviceFound:
            print(valueDict['gateway'], " is online")
            pass
        else:
            print(valueDict['gateway'], " is not online after ", valueDict['timeout'], " seconds")
            raise error.notfind()

    def file_content_get(self, valueDict):
        try:
            hFile = open(valueDict['path'], 'r', encoding='utf8', errors='ignore')
            fileContent = hFile.read() 
            hFile.close()
            #print("File content:\n", fileContent)
            #print(len(fileContent))
            return fileContent
        except:
            raise error.nonamevalue()
            
    def text_search_get(self, valueDict):
        try:
            #print(len(valueDict['text']))
            fileContent = None
            #fileContent = re.findall("[^\r\n]+" + valueDict['regex'] + "", valueDict['text'])
            fileContent = re.findall(valueDict['regex'], valueDict['text'])
            #print("Text search:\n", fileContent)
            return fileContent
        except:
            raise error.nonamevalue()
            
    def text_search_SEARCH_get(self, valueDict):
        try:
            fileContent = None
            fileContent = re.search(valueDict['regex'], valueDict['text'])
            print("Text search:\n", fileContent)
            return fileContent.group(1)
        except:
            raise error.nonamevalue()
            
    def list_length_get(self, valueDict):
        try:
            valueDict['list'] = (valueDict['list'])[1:len(valueDict['list'])]
            valueDict['list'] = (valueDict['list'])[0:len(valueDict['list']) - 1]
            valueDict['list'] = (valueDict['list']).replace("'", "")
            valueDict['list'] = (valueDict['list']).replace(" ", "")
            valueDict['list'] = (valueDict['list']).split(",")
            valueDict['list'] = list(valueDict['list'])
            return len(valueDict['list'])
        except:
            raise error.nonamevalue()
            
    def TFTP_file_list_download_get(self, valueDict):
        try:
            fileList = stringToList(valueDict['list'])
            finalResponse = ""
            for item in fileList:
                command = valueDict['command'] + " " + "\"" + item + "\""
                #print("Command: ", command)
                finalResponse = finalResponse + command + "\n" 
                response = CMD_response_continuously(command, valueDict['prompt'], valueDict['timeout'])
                finalResponse = finalResponse + response + "\n"
            return finalResponse
        except:
            raise error.nonamevalue()
    
    def APK_list_install_get(self, valueDict):
        try:
            APKList = []
            APKList = stringToList(valueDict['list'])
            finalResponse = ""
            for item in APKList:
                if len(item) > 0:
                    command = valueDict['command'] + " \"" + valueDict['folder'] + "\\" + item + "\""
                    print(command)
                    finalResponse = finalResponse + command + "\n" 
                    response = CMD_response_continuously(command, valueDict['prompt'], valueDict['timeout'])
                    finalResponse = finalResponse + response + "\n"
            return finalResponse
        except:
            raise error.nonamevalue()
    
    def folder_files_list_get(self, valueDict):
        try:
            files = listdir(valueDict['folder'])
            files.sort(key = lambda x: os.path.getctime(valueDict['folder'] + "\\" + x))
            ## Order by descending
            files.reverse()
            #print("folder_files_list_get: ", files)
            return files
        except:
            raise error.nonamevalue()
        
    def files_list_delete_get(self, valueDict):
        try:
            FileList = []
            FileList = stringToList(valueDict['list'])
            finalResponse = ""
            #print("files_list_delete_get: ", FileList)
            for item in FileList:
                if len(item) > 0:
                    command = valueDict['command'] + " \"" + valueDict['folder'] + "\\" + item + "\""
                    print("Command: ", command)
                    finalResponse = finalResponse + command + "\n" 
                    response = CMD_response(command)
                    finalResponse = finalResponse + response + "\n"
            return finalResponse
        except:
            raise error.nonamevalue()
    
    def OTA_start_get(self, valueDict):
        ##  Parameters:
        ##      gateway             - gateway name
        ##      gateway_ip          - gateway IP
        ##      gateway_version     - gateway version
        ##      OTA_version         - OTA version
        ##
        ##  OTA command:
        ##      setprop test.ota.init_delay 1
        ##      stop ota
        ##      start ota
        ##
        try:
            gatewayName = valueDict['gateway']
            gatewayIP = valueDict['gateway_ip']
            gatewayVersion = (valueDict['gateway_version']).strip()
            otaVersion = (valueDict['OTA_version']).strip()
            otaCommand = [ \
                "adb -s " + gatewayName + " shell \"setprop test.ota.init_delay 1\"", \
                "adb -s " + gatewayName + " shell \"stop ota\"", \
                "adb -s " + gatewayName + " shell \"start ota\"" \
                ]
            print("Gateway firmware version: ", gatewayVersion, "\nOTA info version: ", otaVersion)
            if gatewayVersion == otaVersion:
                print("No need to OTA.")
                return ""
            else:
                print("Start OTA")
                finalResponse = ""
                for item in otaCommand:
                    finalResponse = finalResponse + item + "\n"
                    response = CMD_response(item)
                    finalResponse = finalResponse + response + "\n"
                    time.sleep(0.5)
                    
                gateway_offline(gatewayName, 300)
                gateway_online(gatewayName, 300)
                CMD_response_continuously("chcp 437 & ping " + gatewayIP + " -t", "Reply from", 300)
                return finalResponse
        except:
            raise error.nonamevalue()
    
    def previous_firmware_version_get(self, valueDict):
        ##  Parameters:
        ##      version             - gateway version
        ##      
        try:
            gatewayVersion = valueDict['version']
            gatewayVersion = re.search("(\d.\d.)(\d+)", gatewayVersion)
            if gatewayVersion:
                temp = gatewayVersion.group(1)
                print("Gateway firmware version: ", temp + gatewayVersion.group(2))
                gatewayVersion = int(gatewayVersion.group(2))
                gatewayVersion -= 1
                print("Previous gateway firmware version: ", temp + str(gatewayVersion))
                return temp + str(gatewayVersion)
            else:
                print("Can NOT find gateway firmware version")
                raise error.nonamevalue()
        except:
            raise error.nonamevalue()
    
    def firmware_version_modify_get(self, valueDict):
        ##  Parameters:
        ##      gateway             - gateway name
        ##      version             - The value will be set to gateway
        ##
        ##  Command:
        ##      adb -s $gateway_name$ shell sed -rn 's/^ro.build.version.release=([^\n]+)$/\1/p' build.prop
        ##      adb -s $gateway_name$ shell "mount -o rw,remount /"
        ##      adb -s $gateway_name$ shell sed "-ir "s/^[#]*\s*ro.build.version.release=.*/ro.build.version.release=$previous_version$/" build.prop"
        ##
        try:
            gatewayName = valueDict['gateway']
            gatewayVersion = valueDict['version']
            command = [ \
                "adb -s " + gatewayName + " shell \"mount -o rw,remount /\"", \
                "adb -s " + gatewayName + " shell sed \"-ir \"s/^[#]*\\s*ro.build.version.release=.*/ro.build.version.release=" + gatewayVersion + "/\" build.prop\"" \
                ]
            finalResponse = ""
            for item in command:
                finalResponse = finalResponse + item + "\n"
                response = CMD_response(item)
                finalResponse = finalResponse + response + "\n"
                time.sleep(0.5)
            print(finalResponse)
        except:
            raise error.nonamevalue()
        #adb -s $gateway_name$ shell sed -rn 's/^ro.build.version.release=([^\n]+)$/\1/p' build.prop
    
    def INI_value_set(self, valueDict):
        ### Set value in INI file.
        ###
        ### Required parameters:
        ###     ini         - INI file path and name.
        ###     scope       - Scope of value.
        ###     value       - Target value.
        ###
        try:
            print(os.getcwd() + "\\" + valueDict['ini'])
            hFile = open(os.getcwd() + "\\" + valueDict['ini'], 'r')
            file_content = hFile.read()
            hFile.close()
            
            file_content = re.sub(valueDict['scope'] + "=[^\r\n]+", valueDict['scope'] + "=" + valueDict['value'], file_content)
            
            hFile = open(os.getcwd() + "\\" + valueDict['ini'], 'w')
            hFile.write(file_content)
            hFile.close()
        except:
            raise error.nonamevalue()
    
    def latest_file_name_get(self, valueDict):
        ##  Get the latest file name in the target folder.
        ##  
        ##  Pre-condition:
        ##      Log file must be named as "0000-00-00-00-00-00-000.txt"
        ##
        ##  Required parameters:
        ##      folder           - The directory of log file
        ##
        ##  Return value:
        ##      Log file full path.
        ##
        ##  This function will check log file continuous until keyword "Finish" is show in file(Timeout: 1800 seconds).
        ##  *Check the latest modified file only
        ##
        try:
            files = listdir(valueDict['folder'])
            files.sort(key = lambda x: os.path.getctime(valueDict['folder'] + "\\" + x))
            ## Order by descending
            files.reverse()
            if len(files) > 0:
                return files[0]
            else:
                return "NULL"
        except:
            raise error.nonamevalue()

    def timestamp_get(self, valueDict):
        ##  Required parameters:
        ##      index_start         - The index of start for substring
        ##      index_end           - The index of end for substring
        ##
        try:
            timestamp = int(datetime.datetime.now().timestamp() * 1000)
            timestamp = str(timestamp)[int(valueDict['index_start']):int(valueDict['index_end'])]
            return timestamp
        except:
            raise error.nonamevalue()

    def TC_8809_upload_verify(self, valueDict):
        ##  1. Load content of gateway log file and filter by "ECLITE".
        ##  2. Verify Data upload to Cloud succeed.
        ##      Keyword: "Publish sensor event to event hub"
        ##  3. Load content of gateway config file.
        ##  4. Verify target scopes existed in gateway config.
        ##  5. Load content of gateway DB file.
        ##  6. Verify upload data match which in DB.
        ##
        ##  Required parameters:
        ##      gateway_log     - The full path of gateway log file.
        ##      gateway_config  - The full path of gateway config file.
        ##      gateway_db      - The full path of gateway DB file.
        ##      uuid_id_mapping - The full path of UUID and ID mapping file.
        ##      scope           - The scope to verify.
        ##          Example: scopeA;scopeB...
        ##
        try:
            valueDict['gateway_log'] in locals().keys()
            valueDict['gateway_config'] in locals().keys()
            valueDict['gateway_db'] in locals().keys()
            valueDict['uuid_id_mapping'] in locals().keys()
            valueDict['scope'] in locals().keys()
        except:
            raise error.nonamevalue()
        
        #   1. Load content of gateway log file and filter by "ECLITE"
        fileContent = file_content(valueDict['gateway_log'])
        #fileContent = text_search(fileContent, "[\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{3}\s+\d+\s+\d+\s\S\sECLITE\s+:\sPublish sensor event to event hub:\s(.*)")
        print(fileContent)
        fileContent = text_search(fileContent, "[\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{3}\s+\d+\s+\d+\s\S\sECLITE\s+:\sPublish sensor event to event hub:\s.*\[(\{\"data_id\":.*\})\]")
        #fileContent = text_search(fileContent, "[\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{3}\s+\d+\s+\d+\s\S\sECLITE\s+:\sPublish sensor event to event hub:\s.*(\{\"data_id\":[^\]]+\})")

        #   1.1 Get scope uuid
        #print(fileContent)
        scopeList = (valueDict['scope']).split(";")
        dataUuidList = []
        for item in scopeList:
            dataUuidList.append(config.get('Smart_Meter_data_UUID', item))
        #print(dataUuidList)
        
        #   1.2 From log file content, filter all data by {"data_id":.....}
        #   Source sample:
        #       06-07 07:29:50.830   172   289 D ECLITE  : Publish sensor event to event hub: {"gateway_id":"7af5e9db-c737-4079-9093-58e99294020d","device_id":"5515deb2-405c-453f-8b3e-e8946e05c9b3","raw":"B+UGBxAeAAAFy8M=","data":[{"data_id":"c4093618-627a-4c99-b190-4845a98c9b1f","timestamp":1623051000000,"value":"379843.000000","format":"real"}],"tags":{}}
        #       06-07 07:29:50.835   172   289 D ECLITE  : Publish sensor event to event hub: {"gateway_id":"7af5e9db-c737-4079-9093-58e99294020d","device_id":"5515deb2-405c-453f-8b3e-e8946e05c9b3","raw":"B+UGBxAeAAAAEuI=","data":[{"data_id":"8fc5c2aa-ecf7-4464-a046-7bf96b590f0b","timestamp":1623051000000,"value":"4834.000000","format":"real"}],"tags":{}}
        tmp = None
        dataList = []
        for i in range(len(fileContent)):
            tmp = re.findall("(\{[^\}]+\})", fileContent[i])
            for item in tmp:
                dataList.append(json.loads(item))  
        #   "dataList" sample:
        #       {'data_id': '1eb9193b-e83e-47e9-a58b-c3bb449f748e', 'timestamp': 1623050555204, 'value': '0.000000', 'format': 'real'}
        #print(len(dataList))
        print(dataList)
        
        #   1.3 From "dataList", filter scope by "dataUuidList"
        dataListFilterScope = []
        dataListFilterScope_dataID = []
        for item in dataList:
            print(item["data_id"])
            if item["data_id"] in dataUuidList and item["data_id"] not in dataListFilterScope_dataID:
                dataListFilterScope.append(item)
                dataListFilterScope_dataID.append(item["data_id"])
        #print(dataListFilterScope)
        #   "dataListFilterScope" is the same with "dataList"
        #print(dataListFilterScope_dataID)
        
        #   2. Verify Data upload to Cloud succeed
        print("Expected scope list:\n", dataUuidList)
        print("Actual scope list with data:\n", dataListFilterScope)
        result = False
        #print("Length of dataListFilterScope: ", len(dataListFilterScope), "\nLength of dataUuidList: ", len(dataUuidList))
        if len(dataListFilterScope) == len(dataUuidList):
            result = True
            print("Target scopes upload to cloud succeed.")
        else:
            print("Target scopes NOT upload to cloud succeed!")
            
        #   3. Load content of gateway config file.
        configContent = file_content(valueDict['gateway_config'])
        
        #   4. Verify target scopes existed in gateway config.
        counter = 0
        for item in dataUuidList:
            if configContent.find(item) != -1:
                print(item, " found in config.json")
                counter += 1
        #print(counter)
        if counter == len(dataUuidList):
            print("Target scopes in config.json.")
        else:
            result = False
            print("Target scopes NOT in config.json.")
        
        #   5. Load content of gateway DB file.
        
        #   5.1 Get timestamp, UUID, value list from data list
        dataTimestampList = []
        dataUuidList = []
        dataValueList = []
        for item in dataListFilterScope:
            dataTimestampList.append(item['timestamp'])
            dataUuidList.append(item['data_id'])
            dataValueList.append(item['value'])
        #print(dataTimestampList)
        #print(dataUuidList)
        #print(dataValueList)
            
        #   5.2 Get data UUID and data ID mapping
        fileContent = file_content(valueDict['uuid_id_mapping'])
        dataUuidIdDict = {}
        for item in dataUuidList:
            tmp = re.search(item + "\s+(\d+)", fileContent)
            if tmp:
                dataUuidIdDict[item] = tmp.group(1)
        #print(dataUuidIdDict)
            
        #   5.3 Filter DB data by timestamp
        fileContent = file_content(valueDict['gateway_db'])
        dbDataList = []
        for i in range(len(dataTimestampList)):
            #   Source sample: 56|163||1623746427715|1|53|56
            tmp = re.search("(.*\|" + dataValueList[i] + "\|.*\|" + str(dataTimestampList[i]) + "\|.*\|" + dataUuidIdDict[dataUuidList[i]] + ")\n", fileContent)
            if tmp:
                print("Found in DB: " + tmp.group(1))
                dbDataList.append(tmp.group(1))
        #print(dbDataList)
        
        #   6. Verify upload data match which in DB.
        if len(dbDataList) == len(dataListFilterScope) and len(dbDataList) != 0:
            print("Upload data match which in DB.")
        else:
            result = False
            print("Upload data NOT match which in DB!")

        print(result)
        valueDict['value'] = result
        valueDict['system_value'] = True
        valueDict['criteria'] = "="
        try:
            Verify().verify(valueDict)
        except error.notequalerror:
            raise error.notequalerror()
        except error.equalerror:
            raise error.equalerror()
        except:
            pass
            