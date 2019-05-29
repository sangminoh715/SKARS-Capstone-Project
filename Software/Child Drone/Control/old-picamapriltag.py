import time
import picamera
import apriltag
import cv2
import numpy as np
import math
import threading
from controller import Controller
# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

##########################################################################

class Parameters(object):
    def __init__(self):
        self.position = np.matrix([0, 0, 0]) #X,Y,Z,R
        self.velocities = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.float64)
        self.velindex = 0
        self.flatIntegral = np.matrix([0, 0, 0]) #X,Y,Z
        self.last_time = time.time()


    def reset(self):
        self.position = np.array([0, 0, 0, 0])
        self.velocities = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.velindex = 0
        self.integral = np.array([0, 0, 0])
        self.last_time = time.time()

    def add(self, vector, current_time):
        delta_t = current_time - self.last_time
        self.last_time = current_time
        curvel = np.subtract(vector.transpose(), self.position)/delta_t
        # print(curvel.shape)
        # print(curvel)
        print(self.velocities)
        self.velocities[self.velindex] = np.float64(curvel)
        # print(self.velocities)
        self.velindex  = (self.velindex + 1)%3
        # print(self.velindex)
        # integral = ((self.integral[0] + vector[0]) * delta_t, (self.integral[1] + vector[1])*delta_t, (self.integral[2], vector[2])*delta_t)
        self.flatIntegral = np.add(self.flatIntegral, 	vector.transpose()* delta_t)
        self.position = vector.transpose()

    def getVel(self):
        return np.sum(self.velocities, axis=0)

    def getPos(self):
    	return self.position

    def getInt(self):
    	return self.flatIntegral


    def printData():
        print("POSITION:", self.position)
        print("VELOCITY:", self.velocities)
        print("INTEGRAL:", self.Integral)

    
class ImageProcessor(threading.Thread):
    def __init__(self, width, height, parameters):
        super(ImageProcessor, self).__init__()
        
        self.height = height
        self.width = width
        
        self.detector = apriltag.Detector()
        self.tag_size = 3.0
        self.parameters = (0,0,0,0) #x,y,z,r
       	self.paramstruct = Parameters();

        fov_x = 62.2*math.pi/180
        fov_y = 48.8*math.pi/180
        fx = self.width/(2*math.tan(fov_x/2))
        fy = self.height/(2*math.tan(fov_y/2))
        self.camera_params = (fx, fy, width/2, height/2)
        
        self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
        
        self.event = threading.Event()
        self.terminated = False
        # self.paramset = Parameters()
        self.controller = Controller(1, 5, 10)
        self.start()


    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    # Read the image and do some processing on it
                    #Image.open(self.stream)
                    self.img = self.img.reshape((self.height,self.width,3))
                    self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
                    results = self.detector.detect(self.img)
                    for i, detection in enumerate(results):
                        pose, e0, e1 = self.detector.detection_pose(detection,self.camera_params,self.tag_size)
                        mat = np.matrix(pose)
                        # print(mat)
                        T = mat[0:3,3]
                        rz = -math.atan2(mat[1,0],mat[0,0])
                        lock.acquire()
                        self.paramstruct.add(np.matrix(mat[0:3,3]), time.time())
                        
                        # self.parameters = (float(T[0]), float(T[1]), float(T[2]), float(rz))
                        # print(self.parameters)
                        # print("\n\n\n")
                        print("integral:", self.paramstruct.getInt())
                        print("velocity", self.paramstruct.getVel())
                        print("position", self.paramstruct.getPos())
                        lock.release()
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    # Reset the stream and event
                    self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)




        

class piCam(object):
    def __init__(self):
        self.width = 640
        self.height = 480
        self.params = Parameters()
        global pool
        pool = [ImageProcessor(self.width,self.height,self.params) for i in range(4)]
        
    def streams(self):
        global done
        global lock
        while not done:
            with lock:
                if pool:
                    processor = pool.pop()
                else:
                    processor = None
            if processor:
                yield processor.img
                processor.event.set()
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)

    
    def start(self):
        with picamera.PiCamera() as camera:
            width = 640
            height = 480
            camera.sensor_mode = 4
            camera.framerate=10
            camera.exposure_mode = 'sports'
            camera.resolution = (self.width, self.height)
            time.sleep(2)
            camera.capture_sequence(self.streams(), 'bgr', use_video_port=True)

        # Shut down the processors in an orderly fashion
        while pool:
            with lock:
                processor = pool.pop()
                processor.terminated = True
                processor.join()


#######################
cam = piCam()
cam.start()

