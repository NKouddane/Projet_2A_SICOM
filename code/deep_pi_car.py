import logging
import serial
import time
import cv2
import datetime
import struct
from hand_coded_lane_follower import HandCodedLaneFollower
#from objects_on_road_processor import ObjectsOnRoadProcessor

_SHOW_IMAGE = True # Activated by default to show the road

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


class DeepPiCar(object):

    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 240

    def __init__(self):
        """ Init camera """

        logging.debug('Set up camera')
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)

        self.lane_follower = HandCodedLaneFollower(self)
        #self.traffic_sign_processor = ObjectsOnRoadProcessor(self)
        #lane_follower = DeepLearningLaneFollower()

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.video_orig = self.create_video_recorder('../data/tmp/car_video%s.avi' % datestr)
        self.video_lane = self.create_video_recorder('../data/tmp/car_video_lane%s.avi' % datestr)
        self.video_objs = self.create_video_recorder('../data/tmp/car_video_objs%s.avi' % datestr)

        
    def create_video_recorder(self, path):
        return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        
        data = ser.write(struct.pack('>B', 0))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    
        self.camera.release()
        self.video_orig.release()
        self.video_lane.release()
        self.video_objs.release()
        cv2.destroyAllWindows()

    def drive(self, speed=__INITIAL_SPEED):
        """ Main entry point of the car, and put it in drive mode """

        logging.info('Starting to drive at speed %s...' % speed)
       
        
        data = ser.write(struct.pack('>B', 1))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
            
        i = 0

        while self.camera.isOpened():
            _, image_lane = self.camera.read()
            image_objs = image_lane.copy()
            i += 1
            self.video_orig.write(image_lane)

#             image_objs = self.process_objects_on_road(image_objs)
#             self.video_objs.write(image_objs)
#             #Displaying objects detected
#             cv2.namedWindow('Detected Objects',cv2.WINDOW_NORMAL)
#             cv2.resizeWindow('Detected Objects', 1000,1000)
#             show_image('Detected Objects', image_objs)

            image_lane = self.follow_lane(image_lane)
            self.video_lane.write(image_lane)
            #Displaying lines detected
            cv2.namedWindow('Lane Lines',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Lane Lines', 1000,1000)
            show_image('Lane Lines', image_lane)
            
        
            #Exit the program
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break

#     def process_objects_on_road(self, image):
#         image = self.traffic_sign_processor.process_objects_on_road(image)
#         return image

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
    with DeepPiCar() as car:
        car.drive(100)


if __name__ == '__main__':   
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    main()
