import math

class dt_controller(object):

  def __init__(self, period=0.086):
    self.period = period
    self.input_last = 0
    self.input_2_last = 0
    self.output_last = 0
    self.output_2_last = 0
  
  def get_output(self, in_t):
    output = 1*self.output_last - 0*self.output_2_last - 11.24*in_t + 11.25*self.input_last - 0*self.input_2_last
    self.input_2_last = self.input_last
    self.input_last = in_t
    self.output_2_last = self.output_last
    self.output_last = output
    return output  
