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
    MAX = 400
    if input > MAX:
        input = MAX
    if input < -MAX:
        input = -MAX
    return input


def send_impulse(vehicle, cam, batt_center, MAX_RANGE = 1, MIN_V = 0.5, MAX_V = 10, IMPULSE_TIME = 0.2):
    X_SCALAR =  3 #4.75
    XV_SCALAR = 7
    XI_SCALAR = 2.75
    
    Y_SCALAR = 3    #4 WAS GOOD
    YV_SCALAR = 7  #10 WAS GOOD
    YI_SCALAR = 2.75 #4.5

    Z_SCALAR = 2
    ZV_SCALAR = 2 #3
    ZI_SCALAR = 1.5

    x = cam.x
    y = cam.y
    z = cam.z

    vx = cam.vx
    vy = cam.vy
    vz = cam.vz
    
    ix = cam.ix
    iy = cam.iy
    iz = cam.iz

    in_x = 0
    in_y = 0
    in_z = 0    

    
    if abs(x) > MAX_RANGE:
        in_x += X_SCALAR*x
    if abs(vx) > MIN_V and abs(vx) < MAX_V:
        in_x += XV_SCALAR*vx

    if abs(y) > MAX_RANGE:
        in_y += Y_SCALAR*y
    if abs(vy) > MIN_V and abs(vx) < MAX_V:
        in_y += YV_SCALAR*vy

    if abs(z) > MAX_RANGE:
        in_z += Z_SCALAR*z
    if abs(vz) > MIN_V and abs(vz) < MAX_V:
        in_z += ZV_SCALAR*vz

    in_x += XI_SCALAR*ix
    in_y += YI_SCALAR*iy
    in_z += ZI_SCALAR*iz


    #if in_x > 0:
     #   in_x *= 1.25
    in_x = saturate(in_x)
    in_y = saturate(in_y)

    #t = time.time()
    #while (time.time() <= t+IMPULSE_TIME and (in_x != 0 or in_y != 0)):
    #vehicle.channels.overrides = {'1': 1500-in_x,'2': 1500-in_y, '3': batt_canter - in_z}
    #vehicle.channels.overrides = {'2': 1500 - in_y, '3': batt_center-in_z} #Control Y
    #vehicle.channels.overrides = {'1': 1500-in_x, '3' : batt_center-in_z} #Control X
    vehicle.channels.overrides = {'1': 1500-in_x, '3': batt_center-in_z}
    time.sleep(0.05)
    #vehicle.channels.overrides = {'2' : 1500}
    print("X:%f\tVX:%f\tIX:%f\tY:%f\tVY:%f\tIY:%f\tZ:%f\tVZ:%f\tIZ:%f" %(x, vy, ix, y, vy, iy, z, vz, iz))
    print("Xin:%f\tYin:%f\tZin:%f\r\n" %(in_x, in_y, in_z))
    #time.sleep(0.21)

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
print("Ready For Flight")
first_sight = True
while True:
    if cam.x != 0:
        if int(vehicle.channels['5']) < 1200:
            #print("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f" %(cam.x, cam.y, cam.z, cam.r, int(vehicle.channels['1']) - 1500, int(vehicle.channels['2']) - 1500, int(vehicle.channels['3']) - 1000, int(vehicle.channels['4']) - 1500, time.time() - t))
            if(first_sight):
                batt_center = -66.980945348*float(vehicle.battery.voltage)+2441.3654157219
                print(batt_center)
                first_sight = False
            send_impulse(vehicle,cam,int(batt_center))
            #xin = saturate(x_control.get_output(cam.x))
            #yin = saturate(y_control.get_output(cam.y))
            #print("X:%f\tY:%f" %(cam.x, cam.y))
            #print("Xin:%f\tYin:%f" %(xin, yin))
            #print("%f\t%f\t%f" %(cam.x, cam.y, time.time() - t))
            #t = time.time()
            #while (time.time() <= t+CONTROL_PERIOD):
                #vehicle.channels.overrides = {'1': 1500-1.2*xin,'2': 1500+1.2*yin}
                #vehicle.channels.overrides = {'1': 1400+xin} #X_CONTROL
                #vehicle.channels.overrides = {'2': 1485+yin} #Y_CONTROL

    else:
        first_sight = True
        vehicle.channels.overrides = {}
    #time.sleep(0.25)
