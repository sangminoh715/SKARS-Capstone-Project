from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


# Connect to the Vehicle
print('Connecting to vehicle')
vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Arm and takeoff to altitude of 4 meters.
# Start at lower middle of chem lawn facing North.
arm_and_takeoff(4)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

# Move towards upper middle of chem lawn facing North.
print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(-13340851.337261, 4084670.758672, 0)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

# Move towards upper left of chem lawn facing North.
print("Going towards second point for 30 seconds")
point2 = LocationGlobalRelative(-13340934.147152, 4084670.581389, 0)
vehicle.simple_goto(point2)

# sleep so we can see the change in map
time.sleep(30)

# Move down towards lower left of chem lawn facing North.
print("Going towards third point for 30 seconds")
point2 = LocationGlobalRelative(-13340927.774289, 4084634.956807, 0)
vehicle.simple_goto(point2)

# sleep so we can see the change in map
time.sleep(30)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
