from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
from openmv_pi import openMV
from dt_controller import dt_controller
from pid import pid
import time
import math
import serial


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

def send_attitude_target(roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):
    """
    use_yaw_rate: the yaw can be controlled using yaw_angle OR yaw_rate.
                  When one is used, the other is ignored by Ardupilot.
    thrust: 0 <= thrust <= 1, as a fraction of maximum vertical thrust.
            Note that as of Copter 3.5, thrust = 0.5 triggers a special case in
            the code for maintaining current altitude.
    """
    if yaw_angle is None:
        # this value may be unused by the vehicle, depending on use_yaw_rate
        yaw_angle = vehicle.attitude.yaw
        roll_angle = vehicle.attitude.roll + roll_angle
        pitch_angle = vehicle.attitude.pitch + pitch_angle
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    msg = vehicle.message_factory.set_attitude_target_encode(
        0, # time_boot_ms
        1, # Target system
        1, # Target component
        0b00000000 if use_yaw_rate else 0b00000100,
        to_quaternion(roll_angle, pitch_angle, yaw_angle), # Quaternion
        0, # Body roll rate in radian
        0, # Body pitch rate in radian
        math.radians(yaw_rate), # Body yaw rate in radian/second
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

def set_attitude(roll_angle = 0.0, pitch_angle = 0.0,
                 yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                 thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent more often than every
    second, as an ATTITUDE_TARGET order has a timeout of 1s.
    In AC3.2.1 and earlier the specified attitude persists until it is canceled.
    The code below should work on either version.
    Sending the message multiple times is the recommended way.
    """
    send_attitude_target(roll_angle, pitch_angle,
                         yaw_angle, yaw_rate, False,
                         thrust)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(roll_angle, pitch_angle,
                             yaw_angle, yaw_rate, False,
                             thrust)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(0, 0,
                         0, 0, True,
                         thrust)

def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]

def get_angles(cam, pid_x, pid_y, pid_z, pid_r, vehicle):
    x = saturate(pid_x.get_output(cam.x))
    y = saturate(pid_y.get_output(cam.y))
    dt = pid_z.get_dt(10)
    z = pid_z.get_pid(cam.z, dt)
    r = cam.r%360
    if r <= 180:
        r = -r
    else:
        r = 360 - r
    r = r*0.1;

    print("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f"%(cam.x,cam.y,cam.z,cam.r,vehicle.channels['1']-1499,vehicle.channels['2']-1585,vehicle.channels['3']-1001,vehicle.channels['4']-1523,dt))
    #print("%f\t%f"%(cam.y,dt))
    return (x, y, z, r)


def saturate(input):
    MAX = 100
    if input > MAX:
        input = MAX
    if input < -MAX:
        input = -MAX
    return input
"""
# Take off 2.5m in GUIDED_NOGPS mode.
arm_and_takeoff_nogps(2.5)

# Hold the position for 3 seconds.
print("Hold position for 3 seconds")
set_attitude(duration = 3)
"""

# Hover over Apriltag
ser = serial.Serial('/dev/ttyS0',baudrate=115200,timeout=0.1)
cam = openMV(ser)
control_x = dt_controller() 
control_y = dt_controller() 
GAIN_P = 1
GAIN_I = 0.7
GAIN_D = 0.05
I_MAX = 10
pid_z = pid(GAIN_P, GAIN_I, GAIN_D, I_MAX) 
pid_r = pid(GAIN_P, GAIN_I, GAIN_D, I_MAX) 
seen_tag = False
first = True
count = 0

while True:
    cam.update()
    if cam.x != 0:
        if first:
            while not vehicle.armed:
                vehicle.armed = True
                time.sleep(1)
            #vehicle.mode = VehicleMode("GUIDED_NOGPS")
            first = False
            #seen_tag = True
        inputs = get_angles(cam, control_x, control_y, pid_z, pid_r, vehicle)
        #print("X:%f \tY:%f \t Z:%f \tR:%f\r\n"%(inputs))
        #send_attitude_target(roll_angle = inputs[0], pitch_angle = -inputs[1],thrust = 0.5)
        #send_attitude_target(roll_angle = -inputs[0], pitch_angle = inputs[1], use_yaw_rate = True, yaw_rate = 0, thrust = 0.4)
        #send_attitude_target(thrust = 0.45)
        if int(vehicle.channels['5']) < 1200:
            #vehicle.channels.overrides = {'1': 1499-inputs[0],'2': 1585-inputs[1]}
            #vehicle.channels.overrides = {'2': 1585-inputs[1]}
        else:
            vehicle.channels.overrides = {}
    else:
        if seen_tag:
            if count > 10:
                vehicle.mode = VehicleMode("LAND")
                time.sleep(1)
                vehicle.close()
            else:
                count = count+1


