# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 15:22:29 2020

@author: Dustin Lin
"""

import automan.tool.error as error
from automan.tool.verify import Verify
from pathlib import Path
import os.path
import cv2 as CV2
#pip3 install opencv-python
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd() , 'ini' , 'Eonone.conf'),encoding="utf-8")

class verify_pic(object):
    def picture_verify(self,value_dict):
        dicParam = dict(value_dict)
        pic1 = dicParam['path']
        pic2 = dicParam['source_path']
        lessthan = dicParam['lessthan']
        img1 = CV2.imread(pic1)
        img2 = CV2.imread(pic2)
        hash1 = self.dHash(img1)
        hash2 = self.dHash(img2)
        dhashvalue = self.cmpHash(hash1, hash2)
        print(float(dhashvalue) , float(lessthan)) 
        strLocation = os.path.join(os.getcwd(), "log", dicParam["logFolderName"], "score.txt")
        file = open(strLocation,"a")
        file.writelines(pic1 + ":  score===> " + str(dhashvalue) + "\n")
        if (float(dhashvalue) > float(lessthan)) :
            return 1
        
    def dHash(self, image):
        img = CV2.resize(image, (9, 8), interpolation=CV2.INTER_CUBIC)
        gray = CV2.cvtColor(img, CV2.COLOR_BGR2GRAY)
        hash_str = ''
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    def cmpHash(self, hash1, hash2):
        n = 0
        if len(hash1) != len(hash2):
            return -1
        for i in range(len(hash1)):
            if hash1[i] != hash2[i]:
                n = n + 1
        return n