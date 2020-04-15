import sys
sys.path.append('..')
import numpy as np
from flightSim.envs import transfer_function_coef as TF
from flightSim.envs import aerosonde_parameters as MAV
import math

gravity = MAV.gravity
rho = MAV.rho
sigma = 0.000001 
Va0 = MAV.Va0

zeta = 0.707

# Tune throttle first by setting everything to 0 in main

#----------roll loop-------------
w_phi = np.sqrt(TF.a_phi2)  # 6.
delta_a_max, error_phi_max = np.radians(30), 0.2 #  np.radians(30) # Arbitrary
roll_kp = delta_a_max / error_phi_max
roll_kd = (2.0 * zeta * w_phi - TF.a_phi1) / TF.a_phi2

#----------course loop-------------
bandwidth_separation_chi = 1 
Vg = Va0    
w_chi = 0.5 # (1.0 / bandwidth_separation_chi) * w_phi # 0.5
course_kp = (2.5 * zeta * w_chi * Vg) / gravity  
course_ki = 0.001 # (w_chi**2) * Vg / gravity # 0.001

#----------sideslip loop-------------
delta_r_max, error_beta_max = np.radians(30), 1. # Chosen arbitrarily
sideslip_kp = delta_r_max / error_beta_max
w_beta = (TF.a_beta1 + TF.a_beta2 * sideslip_kp) / (2.0 * zeta)
sideslip_ki = (w_beta**2) / TF.a_beta2 #1

#----------yaw damper-------------
yaw_damper_tau_r = 0.05
yaw_damper_kp = 0.05

#----------pitch loop-------------
error_theta_max = np.radians(30)  # Chosen arbitrarily
delta_e_max = np.radians(30)                 # Chosen to be 30 
pitch_kp = np.sign(TF.a_theta3) * delta_e_max / error_theta_max 
w_theta = 0.2 # math.sqrt(TF.a_theta2 + pitch_kp * TF.a_theta3)  # 0.2
pitch_kd = (2.0 * zeta * w_theta - TF.a_theta1) / (TF.a_theta3)
K_theta_DC = (pitch_kp * TF.a_theta3) / (TF.a_theta2 + pitch_kp * TF.a_theta3)

#----------altitude loop-------------
bandwidth_separation_altitude = 3.
Va = Va0                          
w_altitude = 0.1 # (1.0/bandwidth_separation_altitude) * w_theta # 0.3
altitude_kp = (2.0 * zeta  * w_altitude) / (K_theta_DC * Va)
altitude_ki = (w_altitude**2) / (K_theta_DC * Va)
altitude_zone = 20.0               ######

#---------airspeed hold using throttle---------------
w_v = 2.0 # np.sqrt(TF.a_V2) # 0.3
zeta_throttle = 0.707
airspeed_throttle_ki = (w_v**2) / TF.a_V2
airspeed_throttle_kp = (2. * zeta_throttle * w_v - TF.a_V1 ) / TF.a_V2
