##  Author: Roger Wei
##  Version: v001
##  Date: 2021/02/23
##  History:
##     2021/02/23 v001: Initial version.
##

import sys
import requests, json
import re, datetime, time, math, random
import configparser, os

def put_request(argvScope, argvValue):
    requestUrl = "http://" + simulatorIP + "/api/device/eojs/" \
        + argvDeviceID \
        + argvDeviceIN \
        + "/epcs/" \
        + str(argvScope)
    requestHeaders = {"Content-Type": "application/json"}
    requestBody = argvValue
    #print("API url: " + requestUrl)
    #print("API header: " + str(requestHeaders))
    #print("API body: " + str(requestBody))
    HTTPResponse = requests.put(requestUrl, json={"edt": requestBody}, headers=requestHeaders)
    #print("   HTTP status code\t: ", HTTPResponse.status_code)
    #print("   HTTP response\t: ", HTTPResponse.json())
    
    statusCode = HTTPResponse.status_code
    HTTPResponse = HTTPResponse.json()
    if statusCode != 200:
        print("   ====================================================")
        print("   HTTP PUT request failed! ")
        print("   Status code\t: ", statusCode)
        print("   Response\t: ", HTTPResponse)
        print("   ====================================================")
    
    HTTPResponse['statusCode'] = statusCode
    return HTTPResponse

def hex_string_format(string):
    try:
        returnValue = re.search("0x([^\r\n]+)", string)
        returnValue = (returnValue.group(1)).upper()
    except:
        returnValue = string
    return returnValue

def hex_random_increase(hexValue, digit):
    hexValue = "0x" + hexValue
    hexValue = int(hexValue, 0)
    hexValue = hexValue + int(math.sqrt(int(random.randint(1, hexValue))))
    hexValue = ("%0." + str(digit) + "X") % hexValue
    return hexValue
    
def hex_sqrt(hexValue, digit):
    hexValue = "0x" + hexValue
    hexValue = int(hexValue, 0)
    hexValue = int(math.sqrt(hexValue))
    hexValue = ("%0." + str(digit) + "X") % hexValue
    return hexValue
    
def hex_random(minimum, maximum, digit):
    hexValue = random.randint(minimum, maximum)
    hexValue = ("%0." + str(digit) + "X") % hexValue
    return hexValue
    
def hex_addition(hexSrcValue, hexAddValue, digit):
    hexSrcValue = "0x" + hexSrcValue
    hexAddValue = "0x" + hexAddValue
    hexSrcValue = int(hexSrcValue, 0)
    hexAddValue = int(hexAddValue, 0)
    hexSrcValue = hexSrcValue + hexAddValue
    hexSrcValue = ("%0." + str(digit) + "X") % hexSrcValue
    return hexSrcValue
    
def hex_minus(hexSrcValue, hexAddValue, digit):
    ## "hexAddValue" must less than "hexSrcValue"
    hexSrcValue = "0x" + hexSrcValue
    hexAddValue = "0x" + hexAddValue
    hexSrcValue = int(hexSrcValue, 0)
    hexAddValue = int(hexAddValue, 0)
    hexSrcValue = hexSrcValue - hexAddValue
    hexSrcValue = ("%0." + str(digit) + "X") % hexSrcValue
    return hexSrcValue

def write_config(section, option, value):
    try:
        configPath = os.path.join(os.getcwd(), "simulator_API.ini")
        configHandle = configparser.ConfigParser()
        configHandle.read(configPath, encoding = "utf-8")
        configHandle.set(section, option, value)
        configHandle.write(open(configPath, "w"))
    except:
        #print("Write to config file failed!")
        pass

if __name__ == '__main__':
    ## argv0: Device ID
    ## argv1: Device instance number
    ## argv2: Scope
    ## argv3: Value
    ## argv4: IP address and port, 127.0.0.1:8880
    ## argv5: Time interval(seconds)
    
    global simulatorIP
    global argvDeviceID
    global argvDeviceIN
    global configPath
    global configHandle

    argv = sys.argv[1:]
    print(argv)

    if len(argv) >= 4:
        argvDeviceID = hex_string_format(argv[0])
        argvDeviceIN = hex_string_format(argv[1])
        argvScope = hex_string_format(argv[2])
        argvValue = hex_string_format(argv[3])
        if len(argv) >= 5:
            simulatorIP = argv[4]
        else:
            simulatorIP = "127.0.0.1:8880"
        
        if len(argv) >= 6:
            timeInterval = int(argv[5])
        else:
            timeInterval = 300

        if argvScope == "auto" or argvValue == "auto":
            try:
                configPath = os.path.join(os.getcwd(), "simulator_API.ini")
                configHandle = configparser.ConfigParser()
                configHandle.read(configPath, encoding = "utf-8")
                startDay = configHandle.get('general', "startday")
                normalValue = configHandle.get('0x0287', "normalValue")
                reverseValue = configHandle.get('0x0287', "reverseValue")
                totalValue = configHandle.get('0x027C', "totalValue")
            except:
                print("Can NOT find simulator_API.ini, running with default value.")
                startDay = (datetime.datetime.now()).strftime("%d")
                normalValue = "00004E20"
                reverseValue = "00002710"
                totalValue = "00000000"

            if argvDeviceID == "0287":
                ## === Power Distribution Board ===
                print("Generate data automatically, do NOT close this window.")
                #startDay = (datetime.datetime.now()).strftime("%d")
                ## 0xC0: Measured cumulative amount of electric energy(normal direction).
                ##       Start from 0x00000064.
                ## 0xC1: Measured cumulative amount of electric energy(reverse direction).
                ##       Start from 0x0000000A.
                #normalValue = "000F4240"
                #reverseValue = "0007A120"
                while 1:
                    print("--- " + str(datetime.datetime.now()) + " ---")
                    nowDay = (datetime.datetime.now()).strftime("%d")
                    if nowDay != startDay:
                        startDay = nowDay
                        normalValue = "000F4240"
                        reverseValue = "0007A120"
                        
                        ## Reset 0xC0
                        print("0x" + argvDeviceID + " 0xC0\t: 0x" + normalValue)
                        put_request("C0", normalValue)
                        write_config("0x0287", "normalValue", normalValue)
                        
                        ## Reset 0xC1
                        print("0x" + argvDeviceID + " 0xC1\t: 0x" + reverseValue)
                        put_request("C1", reverseValue)
                        write_config("0x0287", "reverseValue", reverseValue)
                    
                    else:
                        ## Increase random value (1 ~ Square Root of current value).
                        ## Set 0xC0
                        normalValue = hex_random_increase(normalValue, 8)
                        print("0x" + argvDeviceID + " 0xC0\t: 0x" + normalValue)
                        put_request("C0", normalValue)
                        write_config("0x0287", "normalValue", normalValue)
                        
                        ## Set 0xC1
                        reverseValue = hex_random_increase(reverseValue, 8)
                        print("0x" + argvDeviceID + " 0xC1\t: 0x" + reverseValue)
                        put_request("C1", reverseValue)
                        write_config("0x0287", "reverseValue", reverseValue)
             
                    write_config("general", "startDay", startDay)
                    time.sleep(timeInterval)
                    
            elif argvDeviceID == "027C":
                ## === Fuel Cell ===
                print("Generate data automatically, do NOT close this window.")
                #startDay = (datetime.datetime.now()).strftime("%d")
                ## 0xC4: Measured instantaneous power generation output.
                ##       Start from 0x0064.
                ## 0xC5: Measured cumulative power generation output.
                ##       Start from 0x00000000.
                #totalValue = "00000000"
                while 1:
                    print("--- " + str(datetime.datetime.now()) + " ---")
                    nowDay = (datetime.datetime.now()).strftime("%d")
                    if nowDay != startDay:
                        startDay = nowDay
                        
                        ## Reset 0xC4
                        nowValue = hex_random(1, 65535, 4)
                        print("0x" + argvDeviceID + " 0xC4\t: 0x" + nowValue)
                        put_request("C4", nowValue)
                        
                        ## Reset 0xC5
                        totalValue = hex_addition("00000000", nowValue, 8)
                        print("0x" + argvDeviceID + " 0xC5\t: 0x" + totalValue)
                        put_request("C5", totalValue)
                        write_config("0x027C", "totalValue", totalValue)
                    
                    else:
                        ## Increase random value (1 ~ Square Root of current value)
                        ## Set 0xC4
                        nowValue = hex_random(1, 65535, 4)
                        print("0x" + argvDeviceID + " 0xC4\t: 0x" + nowValue)
                        put_request("C4", nowValue)
                        
                        ## Set 0xC5
                        totalValue = hex_addition(totalValue, nowValue, 8)
                        print("0x" + argvDeviceID + " 0xC5\t: 0x" + totalValue)
                        put_request("C5", totalValue)
                        write_config("0x027C", "totalValue", totalValue)
                    
                    write_config("general", "startDay", startDay)
                    time.sleep(timeInterval)
            
            elif argvDeviceID == "027D":
                ## === Storage Battery ===
                if argvScope == "auto":
                    print("Scope can NOT be \"auto\".")
                else:
                    print("Generate data automatically, do NOT close this window.")
                    ## 0xE2: Remaining stored electricity 1, Wh Get.
                    ## 0xE3: Remaining stored electricity 2, Ah Get.
                    ## 0xE4: Remaining stored electricity 3, % Get.
                    if argvScope == "E4":
                        remainingStored = hex_random(1, int("0x64", 0), 4)
                        #print("remainingStored: ", remainingStored, int("0x" + remainingStored, 0))
                        while 1:
                            print("--- " + str(datetime.datetime.now()) + " ---")
                            if int((datetime.datetime.now()).strftime("%f")) % 2 == 0:
                                ## Increase random value (0 ~ (0x64 - current value))
                                currentToTop = hex_minus("64", remainingStored, 2)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + currentToTop, 0), 2), 2)
                                #print("Add increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_addition(remainingStored, increaseValue, 2)
                            else:
                                ## Decrease random value (0 ~ current value)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + remainingStored, 0), 2), 2)
                                #print("Minus increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_minus(remainingStored, increaseValue, 2)
                            print("0x" + argvDeviceID + " 0xE4\t: 0x" + remainingStored)
                            put_request("E4", remainingStored)                     
                            time.sleep(timeInterval)
                        #remainingStored = random.randint(1, 100)
                        #print("remainingStored: ", remainingStored)
                        #while 1:
                        #    print("--- " + str(datetime.datetime.now()) + " ---")
                        #    if int((datetime.datetime.now()).strftime("%f")) % 2 == 0:
                        #        ## Increase random value (0 ~ (100 - current value))
                        #        currentToTop = 100 - remainingStored
                        #        increaseValue = int(math.sqrt(random.randint(0, currentToTop)))
                        #        print("Add increaseValue: ", increaseValue)
                        #        remainingStored = remainingStored + increaseValue
                        #    else:
                        #        ## Decrease random value (0 ~ current value)
                        #        increaseValue = int(math.sqrt(random.randint(0, remainingStored)))
                        #        print("Minus increaseValue: ", increaseValue)
                        #        remainingStored = remainingStored - increaseValue
                        #    print("0x" + argvDeviceID + " 0xE4\t: 0x" + str(remainingStored))
                        #    put_request("E4", str(remainingStored))                     
                        #    time.sleep(timeInterval)
                    elif argvScope == "E3":
                        remainingStored = hex_random(1, int("0x118E", 0), 4)
                        print("remainingStored: ", remainingStored, int("0x" + remainingStored, 0))
                        while 1:
                            print("--- " + str(datetime.datetime.now()) + " ---")
                            if int((datetime.datetime.now()).strftime("%f")) % 2 == 0:
                                ## Increase random value (0 ~ (0x231E - current value))
                                currentToTop = hex_minus("231E", remainingStored, 4)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + currentToTop, 0), 4), 4)
                                print("Add increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_addition(remainingStored, increaseValue, 4)
                            else:
                                ## Decrease random value (0 ~ current value)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + remainingStored, 0), 4), 4)
                                print("Minus increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_minus(remainingStored, increaseValue, 4)
                            print("0x" + argvDeviceID + " 0xE3\t: 0x" + remainingStored)
                            put_request("E3", remainingStored)                     
                            time.sleep(timeInterval)
                    else:
                        remainingStored = hex_random(1, int("0x0007A11F", 0), 8)
                        #print("remainingStored: ", remainingStored, int("0x" + remainingStored, 0))
                        while 1:
                            print("--- " + str(datetime.datetime.now()) + " ---")
                            if int((datetime.datetime.now()).strftime("%f")) % 2 == 0:
                                ## Increase random value (0 ~ (0xFFFFFFFF - current value))
                                currentToTop = hex_minus("000F423F", remainingStored, 8)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + currentToTop, 0), 8), 8)
                                #print("Add increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_addition(remainingStored, increaseValue, 8)
                            else:
                                ## Decrease random value (0 ~ current value)
                                increaseValue = hex_sqrt(hex_random(0, int("0x" + remainingStored, 0), 8), 8)
                                #print("Minus increaseValue: ", increaseValue, int("0x" + increaseValue, 0))
                                remainingStored = hex_minus(remainingStored, increaseValue, 8)
                            print("0x" + argvDeviceID + " 0xE2\t: 0x" + remainingStored)
                            put_request("E2", remainingStored)                     
                            time.sleep(timeInterval)
            else:
                print("Not support \"auto\" mode.")
        else:
            HTTPResponse = put_request(argvScope, argvValue)
            print("Status code\t: ", HTTPResponse['statusCode'])
            print("Response\t: ", HTTPResponse)
    else:
        print("Usage\t-\n")
        print("[0]\t: Device ID")
        print("[1]\t: Device instance number")
        print("[2]\t: Scope")
        print("[3]\t: Value")
        print("[4]\t: IP address and port. Default: 127.0.0.1:8880")
        print("[5]\t: Time interval(seconds), for \"auto\" mode used. Default: 300 seconds")
        print("*All value must be HEX string(ex. 0x0000)\n")
        print("Devices that support generating data automatically:")
        print("  0x027C - Fuel Cell\t\t\t: Set [2] or/and [3] to \"auto\"")
        print("  0x0287 - Power Distribution Board\t: Set [2] or/and [3] to \"auto\"")
        print("  0x027D - Storage Battery\t\t: Set [3] to \"auto\"")
