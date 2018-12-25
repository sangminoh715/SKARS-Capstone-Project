import RPi.GPIO as GPIO
import sys
import time

''' 
Extends the linear actuator arm to its full length
'''
def extend():
	# Setup
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(32, GPIO.OUT)
	   
	pwm = GPIO.PWM(32, 50) # 50 Hz -> 20 ms period

	# Extend Arm
	print("Extending arm...\n")
	pwm.start(10)
	time.sleep(22)

	# Cleanup
	pwm.stop()
	GPIO.cleanup()
	print("Done")
	exit(0)
	
''' 
Retracts the linear actuator arm to its minimum length
'''
def retract():
	# Setup
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(32, GPIO.OUT)
	   
	pwm = GPIO.PWM(32, 50) # 50 Hz -> 20 ms period

	# Retract Arm
	print("Retracting arm...\n")
	pwm.start(5)
	time.sleep(22)

	# Cleanup
	pwm.stop()
	GPIO.cleanup()
	print("Done")
	exit(0)	
	
if __name__ == "__main__":
	if sys.argv[1] == "0":
		extend()
	elif sys.argv[1] == "1":
		retract()
	else:
		print("Unrecognized Command\n")
		exit(0)