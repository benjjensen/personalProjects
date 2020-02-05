import numpy as np 
import random 
import Parameters as P 

class Dynamics:

    def __init__(self): 
 
        self.state = np.matrix([[P.theta1_0],          # z initial position
                                [P.theta2_0],      # Theta initial orientation
                                [P.theta1_dot_0],       # zdot initial velocity
                                [P.theta2_dot_0]], dtype=float)  # Thetadot initial velocity

        # Uncertainty model
        # alpha = P.uncertainty    # uncertainy parameter
        self.m1 = P.m1 # * (1+2*alpha*np.random.rand() - alpha)
        self.m2 = P.m2 # * (1+2*alpha*np.random.rand()-alpha)
        self.L1 = P.L2  # * (1+2*alpha*np.random.rand() - alpha)
        self.L2 = P.L2
        self.g = P.g
        # self.F = 0.0

    def propagateDynamics(self, u):

        # Integrate ODE
        k1 = self.derivatives(self.state, u)
        k2 = self.derivatives(self.state + P.Ts/2*k1, u)
        k3 = self.derivatives(self.state + P.Ts/2*k2, u)
        k4 = self.derivatives(self.state + P.Ts*k3, u)
        self.state += P.Ts/6 * (k1 + 2*k2 + 2*k3 + k4)

    def derivatives(self, state, u):

        theta1 = state.item(0)
        theta2 = state.item(1)
        theta1_dot = state.item(2)
        theta2_dot = state.item(3)

        theta1_ddot = ( ((self.m2 * P.g * np.sin(theta2) * np.cos(theta1-theta2)) \
                        - (self.m2 * np.sin(theta1 - theta2))*(self.L1*(theta1_dot**2)*np.cos(theta1-theta2) + self.L2*(theta2_dot**2)) \
                        - (self.m1 + self.m2)*P.g*np.sin(theta1))  \
                            / (self.L1*(self.m1+self.m2*(np.sin(theta1-theta2)**2))) )
        theta2_ddot = ( ((self.m1+self.m2)*(self.L1*(theta1_dot**2)*np.sin(theta1-theta2)- P.g*np.sin(theta2) + P.g*np.sin(theta1)*np.cos(theta1-theta2)) \
                            +self.m2*self.L2*(theta2_dot**2)*np.sin(theta1-theta2)*np.cos(theta1-theta2)) \
                            / (self.L2*(self.m1 + self.m2*(np.sin(theta1-theta2)**2))))


        xdot = np.matrix([ [theta1_dot], [theta2_dot], 
                            [theta1_ddot], [theta2_ddot] ])

        return xdot

    def outputs(self):

        theta1 = self.state.item(0)
        theta2 = self.state.item(1)

        return [z, theta]
        
    def states(self):
        return self.state.T.tolist()[0]