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
	# kp = np.array([3, 3, 2])
	# kd = np.array([7, 4.5, 2])
	# ki = np.array([2.75, 2.75, 1.5])
	#X: 3.5, 4.5, 3.5
	#Y: 3, 4.5, 2.75
	kp = np.array([5, 7, 2])
	kd = np.array([8, 9, 2])
	ki = np.array([4, 5, 1.5])
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

	print("Starting!!!!")
	first = True
	while True:
		#TODO:  limi the amount fo time responding ot one april tag read
		#actually control the drone
		#cap values if necessary
		control.remove_controller_override()

		tempParams = ourParams.getParams()
		multMat = np.multiply(deezGains, tempParams)
		thrustvals = np.sum(multMat, axis=0)
		rz = ourParams.getRz()

		if tempParams[0,0] != 0:
			#if first:
		    #	control.setMode("GUIDED_NOGPS")
			# print("Y: %f\tYv: %f\tYi: %f\t" %(tempParams[0,1],tempParams[1,1],tempParams[2,1]))
			# print("PITCH:", -thrustvals[1]) #X,Y,Z
			print("X: %f\tXv: %f\tXi: %f\t" %(tempParams[0,1],tempParams[1,1],tempParams[2,1]))
			print("Roll:", thrustvals[1]) #X,Y,Z
			# control.send_attitude_target(roll_angle = 0.0, pitch_angle = 0.0, use_yaw_rate = True, thrust = 0.5)
			# print(tempParams[0,1])
			# print("THRUSTVALS", thrustvals)
			# print("THRUST:", thrustvals[2]) #X,Y,Z
			# print(ourParams.getVel())
			control.move_drone_nogps(thrust=0, roll=-thrustvals[0], pitch=-thrustvals[1], yaw=0, duration=0)
			time.sleep(0.5)
			# control.move_drone_nogps(thrust=0, roll=0, pitch=-thrustvals[1], yaw=0, duration=0)
		else:
			# print("else")
			control.setMode("STABILIZE")
			first = True
			control.remove_controller_override()


