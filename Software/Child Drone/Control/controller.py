from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
from dt_controller import dt_controller
import numpy as np


class Controller(object):
	def __init__(self, kp, kd, ki):
		self.kp = kp
		self.kd = kd
		self.ki = ki
		self.vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)
		print("connected to vehicle")
		self.dirbias = np.matrix([0, 0, 1])


	def sendImpulse(self, position, velocity, integral, rot):
		print("here")