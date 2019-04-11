# child_com.py: Runs on Raspberry Pi on child drone

import subprocess
import time

parent_status = 1
parent_gps = None

while (1):

    # Read parent status + GPS coordinate
    ssh = subprocess.Popen(['ssh', 'aditya_wadaskar@csil.cs.ucsb.edu', 'cat', '/fs/student/aditya_wadaskar/capstone/communications/parent_status'], stdout=subprocess.PIPE)
    line_num = 0
    for line in ssh.stdout:
        if line_num == 0:
            parent_status = int(chr(line[0]))
            line_num += 1
        else:
            parent_gps = str(line)[2:-3]
    
    # TODO: Perform action based on parent status and current child status
    
    # Update child status
    child_status = 1 # Arbitrary for testing

    # Write child status locally
    f = open("child_status", "w")
    f.write(str(child_status) + "\n") # Write child state
    f.close()

    # Send child_status file to CSIL
    subprocess.Popen(["scp", "/home/aditya_wadaskar/communications/child_status", "aditya_wadaskar@csil.cs.ucsb.edu:/fs/student/aditya_wadaskar/capstone/communications/child_status"])
    
    time.sleep(1)
    
