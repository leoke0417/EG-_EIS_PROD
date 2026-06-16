'''
Created on 2010/12/20

0 Mon Dec 20 15:36:16 2010

@author: panda.huang
'''
#pip install pipwin
#pipwin install pyaudio
from httplib2 import Http
from json import dumps
import cv2

def dHash(img):
    img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def cmpHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

if __name__ == "__main__":
    img1 = cv2.imread("./pic/test/app1.png")
    img2 = cv2.imread("./pic/test/app2.png")
    hash1 = dHash(img1)
    hash2 = dHash(img2)
    n1 = cmpHash(hash1, hash2)
    print('aHash：', n1)    
    

