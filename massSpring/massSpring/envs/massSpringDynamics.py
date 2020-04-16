import numpy as np 

class MassSpringDynamics:

    def __init__(self, m, k, b, len, ts):

        self.state = np.matrix([[0.0], [0.0]])

        self.m = m 
        self.k = k 
        self.b = b 
        self.ell = len
        self.Ts = ts

        # # Uncertainty model                                       # UNCERTAINTY 
        # alpha = P.uncertainty     # uncertainy parameter
        # self.m = P.m * (1+2*alpha*np.random.rand() - alpha)
        # self.k = P.k* (1+2*alpha*np.random.rand() - alpha)
        # self.b = P.b * (1+2*alpha*np.random.rand()-alpha)
        # self.ell = P.ell * (1+2*alpha*np.random.rand() - alpha)

    def propagateDynamics(self, u):

        # Integrate ODE
        k1 = self.derivatives(self.state, u)
        k2 = self.derivatives(self.state + self.Ts/2*k1, u)
        k3 = self.derivatives(self.state + self.Ts/2*k2, u)
        k4 = self.derivatives(self.state + self.Ts*k3, u)
        self.state += self.Ts/6 * (k1 +2*k2+2*k3+k4)

    def derivatives(self, state, u):

        z = state.item(0)
        zdot = state.item(1)
        F = u

            # Equations of motion go here 
        M = np.matrix([1.0])
        C = np.matrix([F - self.b*zdot - self.k*z])

        tmp = np.linalg.inv(M)*C
        zddot = tmp.item(0)
        xdot = np.matrix([[zdot], [zddot]])
        return xdot

    def outputs(self):

        z = self.state.item(0)
        # z_m = z + random.gauss(0, 0.01)
        return [z_m]
        
    def states(self):
        return np.array([ self.state.item(0), self.state.item(1)])
        # return self.state.T.tolist()[0]

    def reset(self):
        self.state = np.matrix([[0.0], [0.0]])