#Import Functions
import serial
import string
import time
import threading

class openMV(object):
    def __init__(self, ser):
        self.ser = ser
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.vx_now = 0
        self.vy_now = 0
        self.vx_last = 0
        self.vy_last = 0
        self.vx_2_last = 0
        self.vy_2_last = 0
        self.current_time = 0
        self.previous_time = time.time()
        self.line = ""
        self.lock = threading.Lock()
        self.count = 0
    def update(self):
        try:
            self.lock.acquire()
            #self.ser.reset_input_buffer()
            self.line = self.ser.readline()
            words = string.split(self.line,",")
            self.line = ""
            if len(words) == 8 and words[0] == 'X' and words[2] == 'Y' and words[4] == 'Z' and words[6] == 'R':
                self.current_time = time.time()
                delta_t = self.current_time - self.previous_time
                self.previous_time = self.current_time
                tmpx = float(words[1])
                tmpy = float(words[3])
                self.z = float(words[5])
                self.r = float(words[7])

                self.vx_now = (tmpx - self.x)/delta_t
                self.vy_now = (tmpy - self.y)/delta_t

                self.vx = (self.vx_now + self.vx_last + self.vx_2_last)/3
                self.vy = (self.vy_now + self.vy_last + self.vy_2_last)/3

                self.vx_2_last = self.vx_last
                self.vy_2_last = self.vy_last

                self.vx_last = self.vx_now
                self.vy_2_last = self.vy_now

                self.x = tmpx
                self.y = tmpy
                self.count = 0
            else:
                if self.count < 10:
                    self.count += 1
                else:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                    self.r = 0
                    self.vx = 0
                    self.vy = 0
        finally:
            self.lock.release()
