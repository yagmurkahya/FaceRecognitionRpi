#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
import cv2
import takepic as t
now = datetime.datetime.now()


t.takepic()


def mails():
 content="RAPOR"
 msg=MIMEMultipart()
 k="someone tried to enter the house on time "+str(now.strftime("%Y-%m-%d %H:%M:%S"))
 text = MIMEText(k)
 msg.attach(text)
 img_data = open("/home/pi/Desktop/y2tube/dataset1/NewPicture.jpg", 'rb').read()
 image = MIMEImage(img_data, name=os.path.basename("/home/pi/Desktop/y2tube/dataset1/NewPicture.jpg"))
 msg.attach(image)

 mail=smtplib.SMTP("smtp.gmail.com",587)

 mail.ehlo()


 mail.starttls()


 mail.login("yagmurrkahya22@gmail.com","*******")
 mail.sendmail("yagmurrkahya22@gmail.com","yagmurrkahyaa@gmail.com",msg.as_string())





mails()

