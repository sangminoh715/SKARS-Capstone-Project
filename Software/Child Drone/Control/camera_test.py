import serial
import time
from openmv_pi import openMV

ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=0.1)
cam = openMV(ser)

last_time = time.time()

while True:
    cam.update()
    current_time = time.time()
    delta_t = current_time - last_time
    last_time = current_time
    print("X:%f\tY:%f\tZ:%f\tR:%f\tvX:%f\tvY:%f\tT:%f"%(cam.x,cam.y,cam.z,cam.r,cam.vx,cam.vy,delta_t))

