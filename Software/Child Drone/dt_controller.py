import time
import math

class controller(object):

  def __init__(self, period=0.086):
    self.period = period
    self.input_last = 0
    self.output_last = 0
    self.last_time = time.time()
  
  def get_output(self, input):
    current_time = time.time()
    num_cycles = round((current_time - self.last_time)/self.period)
    if(num_cycles > 1):
      self.input_last = (input - self.input_last)*(num_cycles - 1)/num_cycles
    output = 0.1513*self.output_last - 3.1332*input + 3.098*self.input_last
    self.input_last = input
    self.output_last = output
    self.last_time = current_time()
    return output  
