"""
Class to determine wind velocity at any given moment,
calculates a steady wind speed and uses a stochastic
process to represent wind gusts. (Follows section 4.4 in uav book)
"""
import sys
sys.path.append('..')
from flightSim.envs.tools.transfer_function import transfer_function
import numpy as np 
import math
from flightSim.envs import parameters as P
from flightSim.envs import aerosonde_parameters as MAV

class wind_simulation:
    def __init__(self, Ts):
        # steady state wind defined in the inertial frame ###################
        self._steady_state = P.wind_steadyState

        ### Low Altitude, Light Turbulence ###
        sigma_u = 1.06 # m/s
        sigma_v = 1.06 # m/s
        sigma_w = 0.7 # m/s
        Lu = 200 # m 
        Lv = 200 # m 
        Lw = 50 # m

        Va = 25 # m/s ######################################

        a1 = sigma_u * math.sqrt(2.0*Va / (np.pi*Lu))
        a2 = sigma_v * math.sqrt(3.0*Va / (np.pi * Lv))
        a3 = a2 * (Va/(Lv*math.sqrt(3.0)))
        a4 = sigma_w * math.sqrt(3.0 * Va / (np.pi*Lw))
        a5 = a4 * (Va / (Lw * math.sqrt(3.0)))
        b1 = (Va/Lu)
        b2 = (Va/Lv)
        b3 = (Va/Lw)

        self.u_w = transfer_function(num=np.array([[a1]]),
                                     den=np.array([[1, b1]]),
                                     Ts=Ts)
        self.v_w = transfer_function(num=np.array([[a2, a3]]),
                                     den=np.array([[1, 2*b2, b2**2.0]]),
                                     Ts=Ts)
        self.w_w = transfer_function(num=np.array([[a4, a5]]),
                                     den=np.array([[1, 2*b3, b3**2.0]]),
                                     Ts=Ts)
        self._Ts = Ts

    def update(self):
        # returns a six vector.
        #   The first three elements are the steady state wind in the inertial frame
        #   The second three elements are the gust in the body frame
        gust = np.array([ self.u_w.update(np.random.randn()),
                          self.v_w.update(np.random.randn()),
                          self.w_w.update(np.random.randn()) ])
        # gust = np.array([ 0., 0., 0. ])
        return np.concatenate(( self._steady_state, gust ))
