import logging
import cv2
import datetime
import serial
import struct
from time import sleep
from time import time
from hand_coded_lane_follower import HandCodedLaneFollower
from panneaux import panneaux

_SHOW_IMAGE = True

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

class LittleBerryCar(object):

    __INITIAL_SPEED = 0
    #Choose a compromise
    __SCREEN_WIDTH = 320  #176        160         352
    __SCREEN_HEIGHT = 240 #144        120         288
    __DATA_TIME     = [0]

    def __init__(self):
        """ Init camera """
        logging.info('Starting LittleBerryCar')
        logging.debug('Set up camera')
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)
        self.lane_follower = HandCodedLaneFollower(self)
        
#     def getSpeed(self):
#         return self.speed
#     
#     def getSpeedTurning(self):
#         return self.speedTurning

    def __enter__(self):
        """ Entering a with statement | magic method"""
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement  | magic method"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)
        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        data = ser.write(struct.pack('>B', 0))
        self.camera.release()
        cv2.destroyAllWindows()

    def drive(self, speed=__INITIAL_SPEED,data_time=__DATA_TIME ):
        """ Allows the car to drive """

        logging.info('Starting to drive at speed %s...' % speed)
        i = 0
        while self.camera.isOpened():
            start=time()
            _, image_lane = self.camera.read()
            i+=1
            if(i==30):
                ret, img = panneaux(self.camera)
                i=0
                if(ret):
                    data = ser.write(struct.pack('>B', 0))
                    #line = ser.readline().decode('utf-8').rstrip()
                    sleep(4)
                    cv2.destroyAllWindows()
            image_lane = self.follow_lane(image_lane)
            show_image('Lane Lines', image_lane)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break
            end=time()
            if len(data_time)<50 :
                data_time.append(end-start)

    def follow_lane(self, image):
        image = self.lane_follower.follow_lane(image)
        return image


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)

def main():
    data_time=[]
    with LittleBerryCar() as car:
        car.drive(140,data_time)
    #calculate the drive function loop's time
    print(sum(data_time)/len(data_time))

if __name__ == '__main__':
    main()
