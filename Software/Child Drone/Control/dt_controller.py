import math

class dt_controller(object):

  def __init__(self, period=0.086):
    self.period = period
    self.input_last = 0
    self.input_2_last = 0
    self.output_last = 0
    self.output_2_last = 0
  
  def get_output(self, in_t):
    output = 0.6908*self.output_last - 0*self.output_2_last - 17.4*in_t + 17.36*self.input_last - 0*self.input_2_last
    self.input_2_last = self.input_last
    self.input_last = in_t
    self.output_2_last = self.output_last
    self.output_last = output
    return output  
