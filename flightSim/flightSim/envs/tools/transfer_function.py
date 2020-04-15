"""
transfer function block (SISO)
"""
import numpy as np
import matplotlib.pyplot as plt

class transfer_function:
    def __init__(self, num, den, Ts):
        # expects num and den to be numpy arrays of shape (1,m) and (1,n)
        m = num.shape[1]
        n = den.shape[1]
        # set initial conditions
        self._state = np.zeros((n-1, 1))
        # make the leading coef of den == 1
        if den[0][0] != 1:
            den = den / den[0][0]
            num = num / den[0][0]
        self.num = num
        self.den = den
        # set up state space equations in control canonical form
        self._A = np.eye(n-1)
        self._B = np.zeros((n-1, 1))
        self._C = np.zeros((1, n-1))
        self._B[0][0] = Ts
        if m == n:
            self._D = num[0][0]
            for i in range(0, m):
                self._C[0][n-i-2] = num[0][m-i-1] - num[0][0]*den[0][n-i-2]
            for i in range(0, n-1):
                self._A[0][i] += - Ts * den[0][i+1]
            for i in range(1, n-1):
                self._A[i][i-1] += Ts
        else:
            self._D = 0.0
            for i in range(0, m):
                self._C[0][n-i-2] = num[0][m-i-1]
            for i in range(0, n-1):
                self._A[0][i] += - Ts * den[0][i]
            for i in range(1, n-1):
                self._A[i][i-1] += Ts

    '''
    def __repr__(self):
        num = self.num.flatten()
        den = self.den.flatten()

        def arr2str(arr):
            order = arr.shape[0] - 1
            ret = ''
            for val in arr: 
                ret += '{:.6g}'.format(val)
                if order > 1:
                    ret += ' s^{:d} + '.format(order)
                    order -= 1
                elif order == 1:
                    ret += ' s + '
                    order -= 1
                    return ret

        num = arr2str(num)
        den = arr2str(den)
        # print(num, len(num))
        divider = max([len(num), len(den)])
        val = 'Transfer function:\n'

        val += '{:{align}{width}}\n'.format(num,
                                    align='^',
                                    width=divider)

        val += '-' * divider
        val += '\n'
        val += '{:{align}{width}}\n'.format(den,
                    align='^',
                    width=divider)

        return val
    '''


    def update(self, u):
        '''Update state space model'''
        self._state = self._A @ self._state + self._B * u
        y = self._C @ self._state + self._D * u
        return y[0][0]

if __name__ == "__main__":
    # instantiate the system
    Ts = 0.01  # simulation step size
    num = np.array([[1, 2]])  # numerator polynomial
    den = np.array([[1, 4, 5, 6]])  # denominator polynomial (no leading 1: s^3+4s^2+5s+6)
    system = transfer_function(num, den, Ts)

    # main simulation loop
    sim_time = 0.0
    time = [sim_time]
    output = [system.update(0.)]
    while sim_time < 10.0:
        u = np.random.randn()  # white noise
        y = system.update(u)  # update based on current input
        sim_time += Ts   # increment the simulation time

        # update date for plotting
        time.append(sim_time)
        output.append(y)

    # plot output vs time
    plt.plot(time, output)
    plt.show()


