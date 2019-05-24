import time
import picamera

with picamera.PiCamera() as camera:
    camera.sensor_mode = 4
    camera.framerate = 20
    camera.resolution = (640, 480)
    camera.exposure_mode = 'sports'
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg',use_video_port=True)
