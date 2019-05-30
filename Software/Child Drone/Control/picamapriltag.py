import time
import picamera
import apriltag
import cv2
import numpy as np
import math
import threading
from parameters import Parameters
# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

##########################################################################


    
class ImageProcessor(threading.Thread):
    def __init__(self, width, height, parameters):
        super(ImageProcessor, self).__init__()
        
        self.height = height
        self.width = width
        
        self.detector = apriltag.Detector()
        self.tag_size = 3.0
        self.parameters = (0,0,0,0) #x,y,z,r
       	self.paramstruct = parameters;
        # self.paramstruct = Parameters();

        fov_x = 62.2*math.pi/180
        fov_y = 48.8*math.pi/180
        fx = self.width/(2*math.tan(fov_x/2))
        fy = self.height/(2*math.tan(fov_y/2))
        self.camera_params = (fx, fy, width/2, height/2)
        
        self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
        
        self.event = threading.Event()
        self.terminated = False
        self.start()


    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.img = self.img.reshape((self.height,self.width,3))
                    self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
                    results = self.detector.detect(self.img)
                    for i, detection in enumerate(results):
                        pose, e0, e1 = self.detector.detection_pose(detection,self.camera_params,self.tag_size)
                        mat = np.array(pose)
                        T = mat[0:3,3]
                        rz = -math.atan2(mat[1,0],mat[0,0])
                        lock.acquire()
                        self.paramstruct.add(np.array(mat[0:3,3]), rz, time.time())
                        lock.release()

                finally:
                    # Reset the stream and event
                    self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)




        

class PiCam(object):
    def __init__(self, multi, parameters):
        self.width = 160 #640
        self.height = 128 #480
        self.params = parameters
        self.multi = multi
        global pool
        if (multi):
            pool = [ImageProcessor(self.width,self.height,self.params) for i in range(8)]
        else:
            pool = [ImageProcessor(self.width,self.height,self.params) for i in range(1)]

        
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
            width = self.width
            height = self.height
            camera.sensor_mode = 4
            camera.framerate=30
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
if __name__ == "__main__":
    paramstruct = Parameters()
    cam = PiCam(True, paramstruct)
    cam.start()

