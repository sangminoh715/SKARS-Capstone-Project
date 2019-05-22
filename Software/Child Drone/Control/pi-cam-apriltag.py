import time
import picamera
import picamera.array
import apriltag
import cv2
import numpy as np
import math
import io

class picam_apriltag:
    def __init__(self):
        self.camera_params = (520.4700622, 529.0770634, 320, 240)
        self.detector = apriltag.Detector()
        self.tag_size = 3.0
        self.parameters = (0,0,0,0) #x,y,z,r
        self.img = np.empty((480 * 640 * 3,),dtype=np.uint8)

    def get_tag_location(self):
        while True:
            self.img = np.empty((480 * 640 * 3,),dtype=np.uint8)
            yield self.img
            self.img = self.img.reshape((480,640,3))
            self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            results = self.detector.detect(self.img)
            for i, detection in enumerate(results):
                if True: #detection.decision_margin > 65:
                    pose, e0, e1 = self.detector.detection_pose(detection,self.camera_params,self.tag_size)
                    mat = np.matrix(pose)
                    R = mat[0:3,0:3].transpose()
                    T = mat[0:3,3]
                    C = np.matmul(R,T)
                    R = -math.atan2(R[1,0],R[0,0])
                    rz = np.matrix([[math.cos(R), -math.sin(R), 0],[math.sin(R), math.cos(R), 0],[0, 0, 1]])
                    C = np.matmul(rz,C)
                    self.parameters = (float(T[0]), float(T[1]), float(T[2]), float(R))
                    print(self.parameters)
            
                
cam = picam_apriltag()
with picamera.PiCamera() as camera:
    camera.sensor_mode = 4
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.exposure_mode = 'sports'
    time.sleep(2)
    camera.capture_sequence(cam.get_tag_location(),'bgr',use_video_port=True)
