import cv2
import numpy as np
import serial
import struct
from time import sleep


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def panneaux(cap):
    stop_cascade = cv2.CascadeClassifier('signalisations/Stop_classificateur.xml')
    
    while True:
        boolean = False
        ret, img = cap.read()
        img = cv2.resize(img, (340, 220))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        panneaux = stop_cascade.detectMultiScale(gray, 1.3,5)
        for (x,y,w,h) in panneaux:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255, 0), 2)
            panneau = img[y:y+h, x:x+w]
            #cv2.imshow('panneau STOP', panneau)
           
            boolean = True
        return img, boolean
    
    
