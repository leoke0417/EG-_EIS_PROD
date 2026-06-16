#coding=utf-8
'''
Created on 2020/12/23

Run this function on respberry pi 4 only
'''
import RPi.GPIO as GPIO
import time

class ble_device(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def pixi_press(self,value_dict):
        # BCM pin number, do not change unless you also switch pin on Pi.
        intChannel = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(intChannel, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.output(intChannel, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(intChannel, GPIO.LOW)
        
        GPIO.cleanup()
        return("PASS")
