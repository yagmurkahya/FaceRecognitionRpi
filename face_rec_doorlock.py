#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2,os
import numpy as np
import pickle
import RPi.GPIO as GPIO
import time
from PIL import Image
from face_lock import unlock,lock
import smtpçalışan as m

id = 0


names = ['None', 'yagmurkahya']


with open('labels', 'rb') as f:
	dicti = pickle.load(f)
	f.close()

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)
minW = 0.1*camera.get(3)
minH = 0.1*camera.get(4)

path = os.path.dirname(os.path.abspath(__file__))

faceCascade = cv2.CascadeClassifier("/home/pi/Desktop/y2tube/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("/home/pi/Desktop/y2tube/trainner.yml")

font = cv2.FONT_HERSHEY_SIMPLEX
prevTime = 0
doorUnlock = False

while True:
    ret, im =camera.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100),flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:

        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
           
            print("Opening Lock")
            unlock(26)
            time.sleep(10)
            lock(26)
            GPIO.cleanup(26)

           
        else:
            

            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            lock(26)
            m.mails()

        cv2.putText(im, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(im, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', im)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
camera.release()
cv2.destroyAllWindows()

