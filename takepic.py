#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
def takepic():
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        cv2.imwrite("/home/pi/Desktop/y2tube/dataset1/NewPicture.jpg",frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()
takepic()

