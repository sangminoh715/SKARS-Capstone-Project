import numpy as np
import time

class Parameters(object):
    def __init__(self):
        self.position = np.array([0, 0, 0]) #X,Y,Z,R
        self.velocities = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.float64)
        self.velindex = 0
        self.flatIntegral = np.array([0, 0, 0]) #X,Y,Z
        self.rz = 0.0
        self.lastTime = time.time()


    def reset(self):
        self.position = np.array([0, 0, 0])
        self.velocities = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.float64)
        self.velindex = 0
        self.integral = np.array([0, 0, 0])
        self.rz = 0.0

    def add(self, vector, rz, current_time):
        vector[1] -= 15
        deltaT = current_time - self.lastTime
        self.rz = rz
        self.lastTime = current_time
        # print(deltaT)
        if deltaT > 1.0:
            self.reset()
            deltaT = 0

        if deltaT != 0:
            curvel = np.subtract(vector.transpose(), self.position)/deltaT
        else:
            curvel = np.array([0, 0, 0])
        self.velocities[self.velindex] = np.float64(curvel)

        self.velindex  = (self.velindex + 1)%3

        self.flatIntegral = np.add(self.flatIntegral, 	vector.transpose()* deltaT)
        self.position = vector.transpose()

    def getRz(self):
        return self.rz

    def getVel(self):
        return np.sum(self.velocities, axis=0)

    def getPos(self):
    	return self.position

    def getInt(self):
    	return self.flatIntegral

    def getParams(self):
        return np.array([self.position, np.sum(self.velocities, axis=0), self.flatIntegral])

    def printData():
        print("POSITION:", self.position)
        print("VELOCITY:", self.velocities)
        print("INTEGRAL:", self.Integral)