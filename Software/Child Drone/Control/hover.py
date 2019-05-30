from picamapriltag import PiCam
from extended_vehicle import DroneControl
import numpy as np
from parameters import Parameters
import threading
import time


def update_camera(cam):
    # while True:
    cam.start()



if __name__ == "__main__":
	kp = np.array([3, 3, 2])
	kd = np.array([7, 7, 2])
	ki = np.array([2.75, 2.75, 1.5])
	deezGains = np.array([kp, kd, ki])
	print(deezGains)
	# deezGains = 
	# print(np.concatenate((kp, kd), axis=1).shape)
	ourParams = Parameters()
	piCam = PiCam(False, ourParams)
	control = DroneControl()

	
	# pidParams = np.concatenate(np.concatenate(kp, kd), ki)
	# print(pidParams.shape)
	t = threading.Thread(target=update_camera, args=(piCam,))
	t.daemon = True
	t.start()
	
	while True:
		#TODO:  limi the amount fo time responding ot one april tag read
		#actually control the drone
		#cap values if necessary
		time.sleep(0.03)
		tempParams = ourParams.getParams()
		# print(tempParams)
		multMat = np.multiply(deezGains, tempParams)
		thrustvals = np.sum(multMat, axis=0)
		# print(thrustvals)
		print(ourParams.getVel())


