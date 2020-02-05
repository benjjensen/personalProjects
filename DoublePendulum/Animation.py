import matplotlib.pyplot as plt 
import numpy as np 
import Parameters as P 
import matplotlib.patches as patches

class Animation:
    def __init__(self):
        plt.style.use('dark_background')
        self.flagInit = True
        self.fig, self.ax = plt.subplots()
        self.handle = []

        self.L1 = P.L1
        self.L2 = P.L2
        self.m1 = P.m1
        self.m2 = P.m2
        self.count = 0

        self.history = []

        plt.axis([ -2*P.L1, 2*P.L1, -2*P.L1, 2*P.L1])
        plt.axis('off')

    def drawSystem(self, u):
        self.count += 1
        theta1 = u[0]       # Angle of upper rod from vertical
        theta2 = u[1]       # Angle of lower rod from vertical

        x, y = self.drawUpperRod(P.x0, P.y0, theta1)
        self.drawUpperBall(x, y)
        x, y = self.drawLowerRod(x, y, theta2)
        self.drawLowerBall(x, y)
        self.history.append( (x,y) )

        self.drawPath()

        if (self.count % 3 == 0):
            filename = 'C:/Users/benjj/Documents/College/gifs/image_%s.png' % self.count
            self.fig.savefig(filename, bbox_inches='tight')
            plt.close(self.fig)

        if self.flagInit == True:
            self.flagInit = False

    def drawUpperRod(self, x0, y0, theta):
        X = [x0, x0 + self.L1*np.sin(theta)]     # X starting/ending points
        Y = [y0, y0 - self.L1*np.cos(theta)]     # Y starting/ending points

        if self.flagInit == True:
            line,  = self.ax.plot(X, Y, lw = P.lw, c = 'red')
            self.handle.append(line)
        else:
            self.handle[0].set_xdata(X)
            self.handle[0].set_ydata(Y)
    
        return X[1], Y[1]

    def drawUpperBall(self, x, y):
        if self.flagInit == True:
            self.handle.append(patches.CirclePolygon( (x,y), radius=P.r, fc = 'white', ec = 'white'))
            self.ax.add_patch(self.handle[1])
        else:
            self.handle[1]._xy = (x, y)

    def drawLowerRod(self, x0, y0, theta):
        X = [x0, x0 + self.L2*np.sin(theta)]      # X starting/ending points
        Y = [y0, y0 - self.L2*np.cos(theta)]     # Y starting/ending points

        if self.flagInit == True:
            line,  = self.ax.plot(X, Y, lw = P.lw, c = 'red')
            self.handle.append(line)
        else:
            self.handle[2].set_xdata(X)
            self.handle[2].set_ydata(Y)
    
        return X[1], Y[1]

    def drawLowerBall(self, x, y):
        if self.flagInit == True:
            self.handle.append(patches.CirclePolygon( (x,y), radius=P.r, fc = 'gray', ec = 'gray'))
            self.ax.add_patch(self.handle[3])
        else:
            self.handle[3]._xy = (x, y)

    def drawPath(self):
        if len(self.history) > 1:
            i = len(self.history) - 1
            X = (self.history[i-1][0], self.history[i][0])
            Y = (self.history[i-1][1], self.history[i][1])
            self.ax.plot(X, Y, linewidth=1.5, color = 'c', alpha=0.5) 

if __name__ == "__main__":
    simAnimation = Animation()
    theta1 = 0.0
    theta2 = 0.0
    simAnimation.drawSystem([theta1, theta2, 0, 0])
    print('Press key to close')
    plt.waitforbuttonpress()
    plt.close()