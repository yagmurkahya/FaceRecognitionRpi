#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
from PIL import Image
import cv2
import pickle

faceCascade = cv2.CascadeClassifier("/home/pi/Desktop/y2tube/haarcascade_frontalface_default.xml")
# OpenCV paketinde bulunan LBPH (YEREL İKİLİ PATTERNS HISTOGRAMS) yüz tanıyıcı kullanıyoruz.
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Geçerli çalışma dizininin yolunu alınır ve images dizinine gidilir.

baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, "datasetyagmurkahya")

currentId = 1
label_ids={}
y_labels=[]
x_train=[]

#Her görüntü dizinine gider ve görüntüleri arar.
#Görüntü mevcutsa, NumPy dizisine dönüştürüyoruz
for root, dirs, files in os.walk(imageDir):
    print(root, dirs, files)
    for file in files:
        print(file)
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root)
            print(label)

            if not label in label_ids:
                label_ids[label] = currentId
                print(label_ids)
                currentId += 1

#Doğru görüntülere sahip olduğumuzdan emin olmak için yüz algılamayı tekrar gerçekleştiriyoruz.
#Ve sonra kıyaslama verilerini hazırlıyoruz
            id_ = label_ids[label]
            pilImage = Image.open(path).convert("L")
            imageArray = np.array(pilImage, "uint8")
            faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = imageArray[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
# Dizin adlarını ve etiket kimliklerini içeren sözlüğü saklayoruz.
with open("labels", "wb") as f:
    pickle.dump(label_ids, f)
    f.close()
# Verileri eğiterek ve dosyayı kaydediyoruz.

recognizer.train(x_train,np.array(y_labels))
recognizer.save("/home/pi/Desktop/y2tube/trainner.yml")
print(label_ids)

