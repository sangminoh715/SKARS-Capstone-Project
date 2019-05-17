from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
from openmv_pi_threading import openMV
from dt_controller import dt_controller
import time
import math
import serial
import threading


# Connect to the Vehicle
print('Connecting to vehicle')
vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)


def arm_and_takeoff_nogps(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    print("Arming motors")
    # Copter should arm in GUIDED_NOGPS mode
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust)
        time.sleep(0.2)


def saturate(input):
    MAX = 120
    if input > MAX:
        input = MAX
    if input < -MAX:
        input = -MAX
    return input


def send_impulse(vehicle, cam, MAX_RANGE = 1, MIN_V = 1, MAX_V = 15, IMPULSE_TIME = 0.08):
    X_SCALAR = 12
    XV_SCALAR = 10
    Y_SCALAR = 15
    YV_SCALAR = 10

    x = cam.x
    y = cam.y
    vx = cam.vx
    vy = cam.vy

    in_x = 0
    in_y = 0
    
    
    if abs(x) > MAX_RANGE:
        in_x += X_SCALAR*x
        if abs(vx) > MIN_V and abs(vx) < MAX_V:
            in_x += XV_SCALAR*vx

    if abs(y) > MAX_RANGE:
        in_y += Y_SCALAR*y
        if abs(vy) > MIN_V and abs(vx) < MAX_V:
            in_y += YV_SCALAR*vy
    #if in_x > 0:
     #   in_x *= 1.25
    in_x = saturate(in_x)
    in_y = saturate(in_y)

    t = time.time()
    while (time.time() <= t+IMPULSE_TIME and (in_x != 0 or in_y != 0)):
        #vehicle.channels.overrides = {'1': 1500-in_x,'2': 1500-in_y}
        vehicle.channels.overrides = {'2': 1500 -in_y} #Control Y
        #vehicle.channels.overrides = {'1': 1500-in_x} #Control X
    vehicle.channels.overrides = {}
    print("X:%f\tY:%f\tVX:%f\tVY:%f" %(x, y,vx,vy))
    print("Xin:%f\tYin:%f\r\n" %(in_x, in_y))

# Hover over Apriltag
ser = serial.Serial('/dev/ttyS0',baudrate=115200,timeout=0.1)
cam = openMV(ser)

def update_camera(cam):
    while True:
        cam.update()

t = threading.Thread(target=update_camera, args=(cam,))
t.daemon = True
t.start()

x_control = dt_controller(0.08)
y_control = dt_controller(0.08)
CONTROL_PERIOD = 0.08
print("MADE IT HERE")
while True:
    if cam.x != 0:
        if int(vehicle.channels['5']) < 1200:
            #send_impulse(vehicle,cam)
            xin = saturate(x_control.get_output(cam.x))
            yin = saturate(y_control.get_output(cam.y))
            print("X:%f\tY:%f" %(cam.x, cam.y))
            print("Xin:%f\tYin:%f" %(xin, yin))
            #t = time.time()
            #while (time.time() <= t+CONTROL_PERIOD):
            vehicle.channels.overrides = {'1': 1500-1.2*xin,'2': 1500+1.2*yin}
                #vehicle.channels.overrides = {'1': 1400+xin} #X_CONTROL
                #vehicle.channels.overrides = {'2': 1500+yin} #Y_CONTROL
    else:
        vehicle.channels.overrides = {}
        
