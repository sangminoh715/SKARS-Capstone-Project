import subprocess
import time

child_status = 1

while (1):

    # Read child status
    ssh = subprocess.Popen(['ssh', 'aditya_wadaskar@csil.cs.ucsb.edu', 'cat', '/fs/student/aditya_wadaskar/capstone/communications/child_status'], stdout=subprocess.PIPE)
    for line in ssh.stdout:
        child_status = int(chr(line[0]))

    # TODO: Perform action based on child status and current parent status
    
    # Update parent status
    parent_status = 2 # Arbitrary for testing
    
    # Update current GPS reading
    gps_coordinates = "1.2.3.4.5" # Arbitrary for testing
    
    # Write status + GPS coordinates to parent_status
    f = open("parent_status", "w")
    f.write(str(parent_status) + "\n") # Write parent state
    f.write(str(gps_coordinates) + "\n") # Write gps coordinates
    f.close()
    
    # Send parent_status file to CSIL
    subprocess.Popen(["scp", "/home/aditya_wadaskar/communications/parent_status", "aditya_wadaskar@csil.cs.ucsb.edu:/fs/student/aditya_wadaskar/capstone/communications/parent_status"])
    
    time.sleep(1)
