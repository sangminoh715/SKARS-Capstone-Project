import time
import picamera
import apriltag
import cv2
import numpy as np
with picamera.PiCamera() as camera:
    camera.resolution = (1640, 1232)
    camera.framerate = 20
    camera.start_preview()
    time.sleep(2)
    options = apriltag.DetectorOptions()
    camera_params = (520.4700622, 529.0770634, 320, 240)
    tag_size = 3
    detector = apriltag.Detector(options)

    while True:
        camera.capture('foo.jpg')
        img = cv2.imread('foo.jpg',cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(640,480))
        results = detector.detect(img)
        for i, detection in enumerate(results):
            pose, e0, e1 = detector.detection_pose(detection,camera_params,tag_size)
            #if e1 < 0.1:
            mat = np.matrix(pose)
            R = mat[0:3,0:3].transpose()
            T = mat[0:3,3]
            rt = np.matrix([0, 0, 1]).transpose()
            C = np.matmul(R,T)
            Rot = np.matmul(R, rt)
            print(C)
            print(Rot)
            print("\r\n")

    
