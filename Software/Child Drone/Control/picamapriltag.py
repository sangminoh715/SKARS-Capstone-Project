import time
import picamera
import apriltag
import cv2
import numpy as np
import math
import threading

# Create a pool of image processors
done = False
time_last = time.time()
lock = threading.Lock()
pool = []

##########################################################################

class ImageProcessor(threading.Thread):
    def __init__(self, width, height, cam):
        super(ImageProcessor, self).__init__()
        
        self.height = height
        self.width = width
        
        self.detector = apriltag.Detector()
        self.tag_size = 3.0
        self.parameters = (0,0,0,0) #x,y,z,r
       
        fov_x = 62.2*math.pi/180
        fov_y = 48.8*math.pi/180
        fx = self.width/(2*math.tan(fov_x/2))
        fy = self.height/(2*math.tan(fov_y/2))
        self.camera_params = (fx, fy, self.width/2, self.height/2)
        
        self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
        
        self.event = threading.Event()
        self.terminated = False
        self.start()


    def run(self):
        # This method runs in a separate thread
        global done
        global time_last
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
                        cam.current_time = time.time()
                        pose, e0, e1 = self.detector.detection_pose(detection,self.camera_params,self.tag_size)
                        mat = np.matrix(pose)
                        T = mat[0:3,3]
                        rz = -math.atan2(mat[1,0],mat[0,0])
                        self.parameters = (float(T[0]), float(T[1]), float(T[2]), float(rz))
                        print(self.parameters)
                        
                    
                    
                    ####
                    delta_t = cam.current_time - cam.previous_time
                    cam.previous_time = cam.current_time
                    if(delta_t > 0):
                        tmpx = self.parameters[0]
                        tmpy = self.parameters[1]
                        tmpz = self.parameters[2]
                        cam.r = self.parameters[3]
    
                        cam.vx_now = (tmpx - cam.x)/delta_t
                        cam.vy_now = (tmpy - cam.y)/delta_t
                        cam.vz_now = (tmpz - cam.z)/delta_t
    
                        cam.vx = (cam.vx_now + cam.vx_last + cam.vx_2_last)/3
                        cam.vy = (cam.vy_now + cam.vy_last + cam.vy_2_last)/3
                        cam.vz = (cam.vz_now + cam.vz_last + cam.vz_2_last)/3
    
                        cam.vx_2_last = cam.vx_last
                        cam.vy_2_last = cam.vy_last
                        cam.vz_2_last = cam.vz_last
    
                        cam.vx_last = cam.vx_now
                        cam.vy_last = cam.vy_now
                        cam.vz_last = cam.vz_now
    
                        cam.x = tmpx
                        cam.y = tmpy
                        cam.z = tmpz
    
                    
                        if delta_t < 1:
                            cam.ix += cam.x*delta_t
                            cam.iy += cam.y*delta_t
                            cam.iz += cam.z*delta_t
                    
                        if delta_t > 3:
                            cam.x = 0
                            cam.y = 0
                            cam.z = 0
                            cam.r = 0
                            cam.vx = 0
                            cam.vy = 0
                            cam.vz = 0
                            cam.ix = 0
                            cam.iy = 0
                            cam.iz = 0
                            cam.vx_now = 0
                            cam.vx_last = 0
                            cam.vx_2_last = 0
                            cam.vy_now = 0
                            cam.vy_last = 0
                            cam.vy_2_last = 0
                            cam.vz_now = 0
                            cam.vz_last = 0
                            cam.vz_2_last = 0
                    
                    ####
                        
                        
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    # Reset the stream and event
                    t = time.time()
                    print(t - time_last)
                    time_last = t
                    self.img = np.empty((self.width * self.height * 3,),dtype=np.uint8)
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

class piCam(object):
    def __init__(self):
        #Proportional
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0

        #Derivative (Average Across 3 to remove noise)
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.vx_now = 0
        self.vy_now = 0
        self.vz_now = 0
        self.vx_last = 0
        self.vy_last = 0
        self.vz_last = 0
        self.vx_2_last = 0
        self.vy_2_last = 0
        self.vz_2_last = 0

        #Integral
        self.ix = 0
        self.iy = 0
        self.iz = 0

        #Time
        self.current_time = 0
        self.previous_time = time.time()
        
        #Other
        self.count = 0

    def streams(self):
        global done
        while not done:
            with lock:
                if self.pool:
                    print("HELP ME")
                    processor = self.pool.pop()
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
            self.pool = [ImageProcessor(width,height,self) for i in range(4)]
            camera.sensor_mode = 4
            camera.framerate=10
            camera.exposure_mode = 'sports'
            camera.resolution = (width, height)
            time.sleep(2)
            camera.capture_sequence(self.streams(), 'bgr', use_video_port=True)
        
        # Shut down the processors in an orderly fashion
        while self.pool:
            with lock:
                processor = self.pool.pop()
            processor.terminated = True
            processor.join()


cam  = piCam()
cam.start()
