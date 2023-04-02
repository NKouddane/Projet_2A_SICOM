import cv2
import numpy as np
import logging
import math
import datetime
import sys
import numpy.ma as ma
import serial
import struct

def findHSVRange(cap):
    '''
    This is a help function to find HSV color ranges, that will be used in other functions of our robot
    It will cteate trackbars to find optimal range values from the captured images
    '''
    global v1_min, v2_min, v3_min, v1_max, v2_max, v3_max 

    # he function namedWindow creates a window that can be used as a placeholder for images and trackbars.
    # Created windows are referred to by their names.
    cv2.namedWindow("Trackbars", 0)
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255
        for j in 'HSV':
            if j == 'H':
                # create trackbar for Hue from 0 tj 180 degrees
                # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. 
                cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 179, (lambda x: None))
            else:
                cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, (lambda x: None))

    while True:

        
        ret, frame = cap.read()
        frame_to_thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        values = []
        for i in ["MIN", "MAX"]:
            for j in 'HSV':
                v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
                values.append(v)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max =  values

        thresh = cv2.inRange(frame_to_thresh, np.array([v1_min, v2_min, v3_min]), np.array([v1_max, v2_max, v3_max]))
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask)


	
        if cv2.waitKey(1) & 0xFF is ord('q'):
            cv2.destroyAllWindows()
            print("Stop programm and close all windows")
            break
 


