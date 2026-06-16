#coding=utf-8
'''
Created on 2010/12/28

@author: panda.huang
'''
import automan.tool.error as error
from automan.tool.verify import Verify
#pip install pipwin
#pipwin install pyaudio

import speech_recognition
import time
import os
import pyaudio
import wave              #
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini' , 'test.conf'),encoding="utf-8")

class Speech(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def speech_get(self,value_dict):
        local_dict = value_dict
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source: 
    
            print("begin:")                        # print
            r.adjust_for_ambient_noise(source)     #
            audio = r.listen(source)
    
        try:
            Text = r.recognize_google(audio, language=local_dict['language'])     #zh-TW
    
        except r.UnknowValueError:
            Text = "can't trans"
        except r.RequestError as e:
            Text = "can't trans{0}".format(e)
    
        return(Text)