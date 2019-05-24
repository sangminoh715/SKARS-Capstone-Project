# child_com.py: Runs on Raspberry Pi on child drone

import subprocess
from time import sleep
import json
from threading import Thread, Lock

parent_status = "P1"
parent_gps = None
lock = Lock()
child_status = None

def main():

    global parent_gps, parent_status, lock, child_status
    
    thread = Thread(target = get_latest_status_and_gps)
    thread.daemon = True
    thread.start()
    
    # TODO: Initialize child drone code here / connect to vehicle

    while True:
    
        lock.acquire()
        local_parent_status = parent_status
        local_parent_gps = parent_gps
        lock.release()
        
        # Do nothing if parent not hovering
        if local_parent_status == "P1":
            pass
        
        # If parent is hovering stably and child is looking to switch batteries
        elif local_parent_status == "P2" and child_status == "C2":

            # Waypoint navigation
            begin_waypoint_mission(local_parent_gps)
            lock.acquire()
            child_status = "C3"
            update_local_and_CSIL("child_status.txt", child_status)
            print child_status
            lock.release()
            
            # Switch to controls/landing
            controls_waypoint_land()
            lock.acquire()
            child_status = "C4"
            update_local_and_CSIL("child_status.txt", child_status)
            print child_status
            lock.release()
        
        # Parent currently switching batteries
        elif local_parent_status == "P3" and child_status != "C5":
            lock.acquire()
            child_status = "C5"
            update_local_and_CSIL("child_status.txt", child_status)
            print child_status
            lock.release()
        
        # If parent finished switching batteries, child takes off and hovers
        elif local_parent_status == "P4" and child_status != "C1":
            update_local_and_CSIL("parent_status.txt", "P2")
            take_off_and_hover()
            lock.acquire()
            child_status = "C1"
            update_local_and_CSIL("child_status.txt", child_status)
            print child_status
            lock.release()
        
        sleep(0.01)


def get_latest_status_and_gps():

    global parent_gps, parent_status, lock, child_status

    while True:
    
        print "Acquiring lock..."

        lock.acquire()
        
        # Read GPS coordinate
        ssh = subprocess.Popen(['ssh', 'aditya_wadaskar@csil-05.cs.ucsb.edu', 'cat', '/fs/student/aditya_wadaskar/capstone/FinalDemo/parent_coordinates.txt'], stdout=subprocess.PIPE)
        for line in ssh.stdout:
            parent_gps = line
            
        sleep(0.3)
        
        # Read Parent status
        ssh = subprocess.Popen(['ssh', 'aditya_wadaskar@csil-05.cs.ucsb.edu', 'cat', '/fs/student/aditya_wadaskar/capstone/FinalDemo/parent_status.txt'], stdout=subprocess.PIPE)
        for line in ssh.stdout:
            parent_status = str(line[0]) + "" + str(line[1])
            
        sleep(0.3)
        
        # Read Child status
        ssh = subprocess.Popen(['ssh', 'aditya_wadaskar@csil-05.cs.ucsb.edu', 'cat', '/fs/student/aditya_wadaskar/capstone/FinalDemo/child_status.txt'], stdout=subprocess.PIPE)
        for line in ssh.stdout:
            child_status = str(line[0]) + "" + str(line[1])

        lock.release()
        sleep(0.3)

# Write to local file and send to CSIL
def update_local_and_CSIL(file, status):
    status = str(status)
    f = open(file, "w+")
    f.write(status + "\n")
    f.close()
    subprocess.Popen(["scp", "/home/pi/SKARS-Capstone-Project/FinalDemo/" + file, "aditya_wadaskar@csil-05.cs.ucsb.edu:/fs/student/aditya_wadaskar/capstone/FinalDemo/" + file])
    sleep(0.3)


def begin_waypoint_mission(parent_location):
    target = json.loads(parent_location)
    
    latitude = target['lat']
    longitude = target['lon']
    altitude = target['alt']
    
    # TODO: Write waypoint code
    
    pass
    
def controls_waypoint_land():
    # TODO: Implement controls algorithm
    
    pass

def take_off_and_hover():
    # TODO: Take off and hover 10 feet above (or return to base)
    
    pass
    
if __name__ == "__main__":
    main()