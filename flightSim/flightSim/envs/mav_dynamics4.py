"""
mav_dynamics
    - this file implements the dynamic equations of motion for MAV
    - use unit quaternion for the attitude state
    
"""
import sys
sys.path.append('..')
import numpy as np
from math import cos, sin 

# load message types
from flightSim.envs.msg_state import msg_state

from flightSim.envs import aerosonde_parameters as MAV
from flightSim.envs import parameters as P
from flightSim.envs.tools.tools import Quaternion2Euler, Quaternion2Rotation
# from tools.tools import RotateV2B

class mav_dynamics:
    def __init__(self, Ts):
        self._ts_simulation = Ts
        # set initial states based on parameter file
        # _state is the 13x1 internal state of the aircraft that is being propagated:
        # _state = [pn, pe, pd, u, v, w, e0, e1, e2, e3, p, q, r]
        # We will also need a variety of other elements that are functions of the _state and the wind.
        # self.true_state is a 19x1 vector that is estimated and used by the autopilot to control the aircraft:
        # true_state = [pn, pe, h, Va, alpha, beta, phi, theta, chi, p, q, r, Vg, wn, we, psi, gyro_bx, gyro_by, gyro_bz]
        self._state = np.array([[MAV.pn0],  # (0)
                               [MAV.pe0],   # (1)
                               [MAV.pd0],   # (2)
                               [MAV.u0],    # (3)
                               [MAV.v0],    # (4)
                               [MAV.w0],    # (5)
                               [MAV.e0],    # (6)
                               [MAV.e1],    # (7)
                               [MAV.e2],    # (8)
                               [MAV.e3],    # (9)
                               [MAV.p0],    # (10)
                               [MAV.q0],    # (11)
                               [MAV.r0]])   # (12)
        # store wind data for fast recall since it is used at various points in simulation
        self._wind = np.array([[0.], [0.], [0.]])  # wind in NED frame in meters/sec
        self._update_velocity_data()
        # store forces to avoid recalculation in the sensors function
        self._forces = np.array([[0.], [0.], [0.]])
        self._Va = MAV.Va0 #MAV.u0
        self._alpha = np.array([0.0])
        self._beta = np.array([0.0])
        self._chi = 0.
        # initialize true_state message
        self.msg_true_state = msg_state()     

    ###################################
    # public functions
    def update_state(self, delta, wind):
        '''
            Integrate the differential equations defining dynamics, update sensors
            delta = (delta_a, delta_e, delta_r, delta_t) are the control inputs
            wind is the wind vector in inertial coordinates
            Ts is the time step between function calls.
        '''
        # get forces and moments acting on rigid bod
        forces_moments = self._forces_moments(delta)

        # Integrate ODE using Runge-Kutta RK4 algorithm
        time_step = self._ts_simulation
        k1 = self._derivatives(self._state, forces_moments)
        k2 = self._derivatives(self._state + time_step/2.*k1, forces_moments)
        k3 = self._derivatives(self._state + time_step/2.*k2, forces_moments)
        k4 = self._derivatives(self._state + time_step*k3, forces_moments)
        self._state += time_step/6 * (k1 + 2*k2 + 2*k3 + k4)                      
        
        # normalize the quaternion
        e0 = self._state.item(6)
        e1 = self._state.item(7)
        e2 = self._state.item(8)
        e3 = self._state.item(9)
        normE = np.sqrt(e0**2+e1**2+e2**2+e3**2)
        self._state[6][0] = self._state.item(6)/normE
        self._state[7][0] = self._state.item(7)/normE
        self._state[8][0] = self._state.item(8)/normE
        self._state[9][0] = self._state.item(9)/normE

        # update the airspeed, angle of attack, and side slip angles using new state
        self._update_velocity_data(wind)

        # update the message class for the true state
        self._update_msg_true_state()

    ###################################
    # private functions
    def _derivatives(self, state, forces_moments):
        """
        for the dynamics xdot = f(x, u), returns f(x, u)
        """
        # extract the states
        pn = state.item(0)
        pe = state.item(1)
        pd = state.item(2)
        u = state.item(3)
        v = state.item(4)
        w = state.item(5)
        e0 = state.item(6)
        e1 = state.item(7)
        e2 = state.item(8)
        e3 = state.item(9)
        p = state.item(10)
        q = state.item(11)
        r = state.item(12)
        #   extract forces/moments
        fx = forces_moments.item(0)
        fy = forces_moments.item(1)
        fz = forces_moments.item(2)
        l = forces_moments.item(3)
        m = forces_moments.item(4)
        n = forces_moments.item(5)

        phi, theta, psi = Quaternion2Euler(e0, e1, e2, e3)

        # Compute in advance for speed (?)
        c_phi = np.cos(phi)
        s_phi = np.sin(phi)
        c_theta = np.cos(theta)
        s_theta = np.sin(theta)
        c_psi = np.cos(psi)
        s_psi = np.sin(psi)

        # position kinematics
        pn_dot = (np.cos(theta) * np.cos(psi) * u) \
                  + ((np.sin(phi)*np.sin(theta)*np.cos(psi) - np.cos(phi)*np.sin(psi)) * v) \
                  + ((np.cos(phi)*np.sin(theta)*np.cos(psi) + np.sin(phi)*np.sin(psi)) * w)    

        pe_dot = (np.cos(theta)*np.sin(psi) * u) \
                  + ((np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(phi)*np.cos(psi)) * v) \
                  + ((np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)) * w)

        pd_dot = (-1*np.sin(theta)*u) \
                 + ((np.sin(phi)*np.cos(theta)) * v) \
                 + ((np.cos(phi)*np.cos(theta)) * w)

        # position dynamics
        u_dot = (r*v - q*w) + (fx/MAV.mass)    
        v_dot = (p*w - r*u) + (fy/MAV.mass)
        w_dot = (q*u - p*v) + (fz/MAV.mass)

        # rotational kinematics
        e0_dot = 0.5 * ( -p * e1 - q * e2 -r * e3 )
        e1_dot = 0.5 * (p*e0 + r * e2 - q * e3)
        e2_dot = 0.5 * (q * e0 - r * e1 + p * e3)
        e3_dot = 0.5 * (r * e0 + q * e1 - p * e2)

        # rotatonal dynamics
        p_dot = (MAV.gamma1 * p * q - MAV.gamma2 * q * r) + (MAV.gamma3 * l + MAV.gamma4 * n)
        q_dot = (MAV.gamma5 * p * r - MAV.gamma6*(p**2 - r**2)) + (m / MAV.Jy)
        r_dot = (MAV.gamma7 * p * q - MAV.gamma1 * q * r) + (MAV.gamma4 * l + MAV.gamma8 * n)

        # collect the derivative of the states
        x_dot = np.array([ [pn_dot, pe_dot, pd_dot, u_dot, v_dot, w_dot,
                           e0_dot, e1_dot, e2_dot, e3_dot, p_dot, q_dot, r_dot] ]).T  # array -> extra brackets
        return x_dot

    '''
        wind[0:3] = steady state, inertial frame
        wind[3:6] = gusts, body frame
    '''
    def _update_velocity_data(self, wind=np.zeros((6,1))):

        # compute airspeed
        u = self._state[3]
        v = self._state[4]
        w = self._state[5]

        ''' ROTATE wind(Inertial) ->  wind(Body)''' 
        windInInertial = np.array([ [wind.item(0)], [wind.item(1)], [wind.item(2)] ])
        e0, e1, e2, e3 = self._state[6], self._state[7], self._state[8], self._state[9]
        e = np.array([e0, e1, e2, e3])
        R = Quaternion2Rotation(e)
        # phi, theta, psi = Quaternion2Euler(e0, e1, e2, e3)
        # Rv_b = RotateV2B(phi, theta, psi)

        gust = wind[3:6]

        windInBody = R @ windInInertial + gust
        uw = windInBody.item(0)
        vw = windInBody.item(1)
        ww = windInBody.item(2)

        ur = u - uw 
        vr = v - vw
        wr = w - ww
        
        self._Va = np.sqrt( (ur**2) + (vr**2) + (wr**2) )
        # compute angle of attack
        self._alpha = np.arctan(wr /ur)    
        # compute sideslip angle
        self._beta = np.arcsin(vr / self._Va)

        # Compute heading (CHI)
        rates = np.dot(R, self._state[3:6])
        north, east, down = rates.item(0), rates.item(1), rates.item(2)
        # north, east, down = zip(*rates)
        self._chi = np.arctan2(east, north)
        self._gamma = np.arctan2(-down, np.sqrt((north**2) + (east**2)))
        self._Vg = np.sqrt(north**2 + east**2 + down**2)

    def _forces_moments(self, delta):
        """
        return the forces on the UAV based on the state, wind, and control surfaces
        :param delta: np.matrix(delta_a, delta_e, delta_r, delta_t)
        :return: Forces and Moments on the UAV np.matrix(Fx, Fy, Fz, Ml, Mn, Mm)
        """
        delta_a = delta[0]
        delta_e = delta[1]
        delta_r = delta[2]
        delta_t = delta[3]
        e0 = self._state[6]
        e1 = self._state[7]
        e2 = self._state[8]
        e3 = self._state[9]
        phi, theta, psi = Quaternion2Euler(e0, e1, e2, e3)
        _beta = self._beta
        _Va = self._Va
        _alpha = self._alpha
        p = self._state[10]
        q = self._state[11]
        r = self._state[12]

        # Forces:  F = U + Tp + kA + kB
        C_Da = MAV.C_D_0 + MAV.C_D_alpha * _alpha  
        C_La = MAV.C_L_0 + MAV.C_L_alpha * _alpha
        C_Xa = -C_Da * cos(_alpha) + C_La * sin(_alpha)
        C_Xq = -MAV.C_D_q * cos(_alpha) + MAV.C_L_q * sin(_alpha)  
        C_Xde = -MAV.C_D_delta_e * cos(_alpha) + MAV.C_L_delta_e * sin(_alpha)
        C_Z = -C_Da*sin(_alpha) - C_La * cos(_alpha)
        C_Zq = -MAV.C_D_q * sin(_alpha) - MAV.C_L_q * cos(_alpha)
        C_Zde = -MAV.C_D_delta_e * sin(_alpha) - MAV.C_L_delta_e * cos(_alpha)
        
        U = np.array([ (-MAV.mass * MAV.gravity * sin(theta)),
                        (MAV.mass * MAV.gravity * cos(theta) * sin(phi)),
                        (MAV.mass * MAV.gravity * cos(theta) * cos(phi)) ]).T

        # Calculate Tp

        propThrust, propTorque = self._get_thrust(_Va, delta_t)
        Tp = np.array([ (propThrust.item(0)), 
                            (0.0),
                            (0.0) ]).T
       

        k = 0.5 * MAV.rho * (_Va**2) * MAV.S_wing
        A = np.array([ (C_Xa + (C_Xq * MAV.c * q)/(2.0*_Va)),  # Divide by 0 ...?????????????
                        (MAV.C_Y_0+MAV.C_Y_beta*_beta+(MAV.C_Y_p*MAV.b*r/(2.0*_Va)) + (MAV.C_Y_r*MAV.b*r/(2.0*_Va))),
                        (C_Z + (C_Zq*MAV.c*q/(2.0*_Va))) ]).T

        B = np.array([ (C_Xde*delta_e),
                        (MAV.C_Y_delta_a*delta_a + MAV.C_Y_delta_r*delta_r),
                        (C_Zde * delta_e) ]).T

        f = U + Tp + k*A + k*B
        fx, fy, fz = f.item(0), f.item(1), f.item(2) 
        self._forces[0] = fx
        self._forces[1] = fy
        self._forces[2] = fz

        # Torques:  M = k*C + k*D + Qp         
        C = np.array([ (MAV.b*(MAV.C_ell_0 \
                            + (MAV.C_ell_beta*_beta) \
                            + (MAV.C_ell_p*MAV.b*p / (2.0*_Va)) \
                            + (MAV.C_ell_r*MAV.b*r / (2.0*_Va)) )), 
                        (MAV.c * (MAV.C_m_0 + MAV.C_m_alpha * _alpha \
                            + (MAV.C_m_q * MAV.c * q / (2.0*_Va)))),
                        (MAV.b*(MAV.C_n_0 + MAV.C_n_beta * _beta \
                            + (MAV.C_n_p * MAV.b * p / (2.0 * _Va)) \
                            + (MAV.C_n_r * MAV.b * r / (_Va * 2.0)) )) ]).T


        D = np.array([ (MAV.b * (MAV.C_ell_delta_a*delta_a + MAV.C_ell_delta_r*delta_r)),
                        (MAV.c * (MAV.C_m_delta_e * delta_e)),
                        (MAV.b * (MAV.C_n_delta_a * delta_a + MAV.C_n_delta_r * delta_r)) ]).T

        Qp = np.array([ (propTorque.item(0)),
                        (0.0),
                        (0.0) ]).T

        M = k*C + k*D + Qp                             
        Mx, My, Mz = M.item(0), M.item(1), M.item(2)

        return np.matrix([[fx, fy, fz, Mx, My, Mz]]).T    

    def _get_thrust(self, Va, delta_t):
        Vin = MAV.V_max * delta_t
        a = MAV.C_Q0 * MAV.rho * np.power(MAV.D_prop, 5) \
            / ((2.0*np.pi)**2)
        b = (MAV.C_Q1 * MAV.rho*np.power(MAV.D_prop,4) \
            / (2.0*np.pi)) * Va + MAV.KQ**2 / MAV.R_motor 

        c = MAV.C_Q2 * MAV.rho * np.power(MAV.D_prop,3) \
            * (Va**2) - (MAV.KQ / MAV.R_motor) * Vin + MAV.KQ * MAV.i0  
        Omega_op = (-b + np.sqrt(b**2 - 4.0*a*c)) / (2.0*a)     # Only positive root
        J_op = 2.0 * np.pi * Va / (Omega_op * MAV.D_prop)
        C_T = MAV.C_T2 * J_op**2 + MAV.C_T1 * J_op + MAV.C_T0
        C_Q = MAV.C_Q2 * J_op**2 + MAV.C_Q1 * J_op + MAV.C_Q0
        n = Omega_op /(2.0 * np.pi)
        propThrust = MAV.rho * (n**2) * np.power(MAV.D_prop, 4) * C_T 
        propTorque = -MAV.rho * (n**2) * np.power(MAV.D_prop,5) * C_Q

        return propThrust, propTorque

    def _update_msg_true_state(self):
        # update the class structure for the true state:
        #   [pn, pe, h, Va, alpha, beta, phi, theta, chi, p, q, r, Vg, wn, we, psi, gyro_bx, gyro_by, gyro_bz]
        phi, theta, psi = Quaternion2Euler(self._state[6], self._state[7], self._state[8], self._state[9])
        self.msg_true_state.pn = self._state.item(0)
        self.msg_true_state.pe = self._state.item(1)
        self.msg_true_state.h = -self._state.item(2)
        self.msg_true_state.Va = self._Va.item(0)
        self.msg_true_state.alpha = self._alpha.item(0)
        self.msg_true_state.beta = self._beta.item(0)
        self.msg_true_state.phi = phi
        self.msg_true_state.theta = theta
        self.msg_true_state.psi = psi
        self.msg_true_state.Vg = self._Vg 
        self.msg_true_state.gamma = self._gamma           
        self.msg_true_state.chi = self._chi                    
        self.msg_true_state.p = self._state.item(10)
        self.msg_true_state.q = self._state.item(11)
        self.msg_true_state.r = self._state.item(12)
        self.msg_true_state.wn = self._wind.item(0)
        self.msg_true_state.we = self._wind.item(1)

    def reset(self):
        self._state = np.array([[MAV.pn0],  # (0)
                               [MAV.pe0],   # (1)
                               [MAV.pd0],   # (2)
                               [MAV.u0],    # (3)
                               [MAV.v0],    # (4)
                               [MAV.w0],    # (5)
                               [MAV.e0],    # (6)
                               [MAV.e1],    # (7)
                               [MAV.e2],    # (8)
                               [MAV.e3],    # (9)
                               [MAV.p0],    # (10)
                               [MAV.q0],    # (11)
                               [MAV.r0]])   # (12)
        # store wind data for fast recall since it is used at various points in simulation
        self._wind = np.array([[0.], [0.], [0.]])  # wind in NED frame in meters/sec
        self._update_velocity_data()
        # store forces to avoid recalculation in the sensors function
        self._forces = np.array([[0.], [0.], [0.]])
        self._Va = MAV.Va0 #MAV.u0
        self._alpha = np.array([0.0])
        self._beta = np.array([0.0])
        self._chi = 0.
        # initialize true_state message
        self._update_msg_true_state()
