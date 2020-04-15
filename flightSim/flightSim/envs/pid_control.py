"""
pid_control
    - Beard & McLain, PUP, 2012
    - Last Update:
        2/6/2019 - RWB
"""
import sys
import numpy as np
sys.path.append('..')

class pid_control:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0, Ts=0.01, sigma=0.05, limit=1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.Ts = Ts
        self.limit = limit
        self.integrator = 0.0
        self.error_delay_1 = 0.0
        self.error_dot_delay_1 = 0.0
        # gains for differentiator
        self.a1 = (2.0 * sigma - Ts) / (2.0 * sigma + Ts)
        self.a2 = 2.0 / (2.0 * sigma + Ts)

    def update(self, y_ref, y, reset_flag=False):
        if reset_flag == True:
            self.integrator = 0.0
            self.error_delay_1 = 0.0
            self.y_dot = 0.0
            self.y_delay_1 = 0.0
            self.y_dot_delay_1 = 0.0
            

        error = y_ref - y

        # Update the Integrator
        self.integrator = self.integrator \
                            + (self.Ts / 2.0) * (error + self.error_delay_1)
        # Update the Differentiator
        error_dot = self.a1 * self.error_dot_delay_1 \
                        + self.a2 * (error - self.error_delay_1)            

        error_dot = self

        self.theta_dot = self.theta_dot * self.beta + (1 - self.beta) / self.Ts * (theta - self.theta_d1)
        
        # Update P, I, D 
        u = self.kp * error \
            + self.ki * self.integrator \
            + self.kd * error_dot           # TODO: Negative?

        u_sat = self._saturate(u)

        # Anti-Windup
        # if not np.testing.assert_almost_equal(np.abs(self.ki), 0.0):
        if np.abs(self.ki) > 0.00001:
            self.integrator = self.integrator \
                                + (self.Ts / self.ki) * (u_sat - u)

        self.error_delay_1 = error 
        self.error_dot_delay_1 = error_dot

        return u_sat 

    # Derivative is provided
    def update_with_rate(self, y_ref, y, ydot, reset_flag=False):
        if reset_flag == True:
            self.integrator = 0.0
            self.error_delay_1 = 0.0

        error = y_ref - y 
        self.integrator = self.integrator + (self.Ts/2.0) \
                            * (error + self.error_delay_1)
        
        u = self.kp * error \
            + self.ki * self.integrator \
            + self.kd * ydot                # TODO: negative...?

        u_sat = self._saturate(u)

        # Anti-Windup
        if np.abs(self.ki) > 0.00001:       #####
            self.integrator = self.integrator \
                                + (self.Ts / self.ki) * (u_sat - u)
        
        self.error_delay_1 = error
        return u_sat

    def _saturate(self, u):
        # saturate u at +- self.limit
        if u >= self.limit:
            u_sat = self.limit
        elif u <= -self.limit:
            u_sat = -self.limit
        else:
            u_sat = u
        return u_sat

class pi_control:
    def __init__(self, kp=0.0, ki=0.0, Ts=0.01, limit=1.0):
        self.kp = kp
        self.ki = ki
        self.Ts = Ts
        self.limit = limit
        self.integrator = 0.0
        self.error_delay_1 = 0.0

    def update(self, y_ref, y):
        error = y_ref - y

        # Update the Integrator
        self.integrator = self.integrator \
                            + (self.Ts / 2.0) * (error + self.error_delay_1)
        
        # Update P, I
        u = self.kp * error \
            + self.ki * self.integrator 

        u_sat = self._saturate(u)

        # Anti-Windup
        # if np.abs(self.ki) > 0.00001 #not (np.abs(self.ki) == 0.0):
        #     self.integrator = self.integrator \
        #                         + (self.Ts / self.ki) * (u_sat - u)

        self.error_delay_1 = error 
        return u_sat 

    def _saturate(self, u):
        # saturate u at +- self.limit
        if u >= self.limit:
            u_sat = self.limit
        elif u <= -self.limit:
            u_sat = -self.limit
        else:
            u_sat = u
        return u_sat

class pd_control_with_rate:
    # PD control with rate information
    # u = kp*(yref-y) - kd*ydot
    def __init__(self, kp=0.0, kd=0.0, limit=1.0):
        self.kp = kp
        self.kd = kd
        self.limit = limit
        self.integrator = 0.0
        self.error_delay_1 = 0.0

    def update(self, y_ref, y, ydot):
        error = y_ref - y
        u = self.kp * error + self.kd * ydot        # TODO: negative?
        u_sat = self._saturate(u)
        return u_sat 

    def _saturate(self, u):
        # saturate u at +- self.limit
        if u >= self.limit:
            u_sat = self.limit
        elif u <= -self.limit:
            u_sat = -self.limit
        else:
            u_sat = u
        return u_sat
