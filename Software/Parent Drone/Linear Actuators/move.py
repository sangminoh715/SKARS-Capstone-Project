import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
   
pwm = GPIO.PWM(32, 50) # 50 Hz -> 20 ms period
pwm.start(5)

''' 
Function for extending the linear actuator arm
'''
def extend():
	print("Extending arm...\n")
	pwm.ChangeDutyCycle(10)
	time.sleep(22)

'''
Function for retracting the linear actuator arm
'''
def retract():
	print("Retracting arm...\n")
	pwm.ChangeDutyCycle(5)
	time.sleep(22)	

'''	
Main Function Loop	
'''
def main():
	while True:
		user_input = int(input("Please enter command (0 - extend, 1 - retract, 2 - quit): "))

		if user_input == 0:
			extend()

		elif user_input == 1:
			retract()

		elif user_input == 2:
			print("Exiting Program...\n")
			pwm.stop()
			GPIO.cleanup()
			exit(0)

		else:
			print("Unrecognized Command\n")

if __name__ == "__main__":
	main()