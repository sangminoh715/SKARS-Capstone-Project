import math
import time

class pid(object):

    def __init__(self, initial_p=0, initial_i=0, initial_d=0, initial_imax=0):
        # default config file
        self.p_gain = initial_p
        self.i_gain = initial_i
        self.d_gain = initial_d
        self.imax = abs(initial_imax)
        self.integrator = 0
        self.last_error = None
        self.last_error_int = None
        self.last_update = time.time() 

    # __str__ - print position vector as string
    def __str__(self):
        return "P:%s,I:%s,D:%s,IMAX:%s,Integrator:%s" % (self.p_gain, self.i_gain, self.d_gain, self.imax, self.integrator)

    # get_dt - returns time difference since last get_dt call
    def get_dt(self, max_dt):
        now = time.time()
        time_diff = now - self.last_update
        self.last_update = now
        if time_diff > max_dt:
            return 0.0
        else:
            return time_diff

    # get_p - return p term
    def get_p(self, error):
        return self.p_gain * error

    # get_i - return i term
    def get_i(self, error, dt):
        if self.last_error_int is None:
            self.last_error_int = error
        if (self.last_error_int < 0 and error > 0) or (self.last_error_int > 0 and error < 0):
            self.reset_I()
        self.last_error_int = error
        self.integrator = self.integrator + error * self.i_gain * dt
        self.integrator = min(self.integrator, self.imax)
        self.integrator = max(self.integrator, -self.imax)
        return self.integrator

    # get_d - return d term
    def get_d(self, error, dt):
        if self.last_error is None:
            self.last_error = error
        ret = (error - self.last_error) * self.d_gain / dt
        self.last_error = error
        return ret

    # get pi - return p and i terms
    def get_pi(self, error, dt):
        return self.get_p(error) + self.get_i(error,dt)

    # get pid - return p, i and d terms
    def get_pid(self, error, dt):
        return self.get_p(error) + self.get_i(error,dt) + self.get_d(error, dt)

    # get_integrator - return built up i term
    def get_integrator(self):
        return self.integrator

    # reset_I - clears I term
    def reset_I(self):
        self.integrator = 0
