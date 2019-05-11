#Import Functions
import serial
import string
import time

class openMV(object):
    def __init__(self, ser):
        self.ser = ser
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.line = ""
        self.last_time = 0

    def update(self):
        self.ser.reset_output_buffer()
        count = 0
        tmpx = 0
        tmpy = 0
        tmpx_total = 0
        tmpy_total = 0
        tmpz_total = 0
        tmpr_total = 0
        tmpvx = 0
        tmpvy = 0
        for x in range(3):
            self.line = self.ser.readline()
            words = string.split(self.line,",")
            self.line = ""
            if len(words) == 8 and words[0] == 'X' and words[2] == 'Y' and words[4] == 'Z' and words[6] == 'R':
                if count == 0:
                    self.last_time = time.time()
                else:
                    current_time = time.time()
                    delta_t = current_time - self.last_time
                    self.last_time = current_time
                    tmpvx += (float(words[1]) - tmpx)/delta_t
                    tmpvy += (float(wordsd[3]) - tmpy)/delta_t
                tmpx = float(words[1])
                tmpy = float(words[3])
                tmpx_total += tmpx
                tmpy_total += tmpy
                tmpz_total += float(words[5])
                tmpr_total += float(words[7])
                count += 1
        if count > 1:
            self.x = tmpx_total/count
            self.y = tmpy_total/count
            self.z = tmpz_total/count
            self.r = tmpr_total/count
            self.vx = tmpvx/(count - 1)
            self.vy = tmpvy/(count - 1)

