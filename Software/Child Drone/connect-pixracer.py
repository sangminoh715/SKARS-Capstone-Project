
# Import DroneKit-Python
from dronekit import connect, VehicleMode
import time
# Connect to the Vehicle.
print("Connecting to vehicle")
vehicle = connect('/dev/ttyUSB0',baud=115200, wait_ready=True)
vehicle.mode = VehicleMode("GUIDED")
print "Mode: %s" % vehicle.mode.name    # settable

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """


    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(1.5)
time.sleep(5)
vehicle.mode = VehicleMode("LAND")
vehicle.close()


# Close vehicle object before exiting script
vehicle.close()
print("Completed")


