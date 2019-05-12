import threading
import time
from openmv_pi_threading import openMV
import serial


def worker(cam):
    while True:
        cam.update()
        print("Subthread, X:%f\tY:%f" %(cam.x, cam.y))


ser = serial.Serial('/dev/ttyS0',baudrate=115200,timeout=0.1)
cam = openMV(ser)

t = threading.Thread(target=worker, args=(cam,))
t.daemon = True
t.start()

while True:
    time.sleep(1)
    print("Main Thread, X:%f\tY:%f" %(cam.x, cam.y))
