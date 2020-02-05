import numpy as np 
import random

# System Parameters:

m1 = 0.5      # Mass of upper sphere, kg
m2 = 0.5      # Mass of lower sphere, kg
L1 = 0.75      # Length of upper rod, m
L2 = 0.75      # Length of lower rod, m
g = 9.81    # Gravitational constant, m/s^2
x0 = 0
y0 = 0

# Animation Parameters:
lw = 0.4    # Width of rods
r = 0.01    # Radius of spheres


# Initial Conditions:
theta1_0 = (np.random.randint(-20,20,1) * np.pi/20.0) # Initial angle for upper rod from vertical, radians
theta2_0 = (np.random.randint(-20,20,1) * np.pi/20.0)    # Initial angle for lower rod from vertical, radians
theta1_dot_0 = 0
theta2_dot_0 = 0

# Simulation Parameters:
t_start = 0.0
t_end = 10.0
Ts = 0.005   # Sample time
t_plot = 0.1 # Plotting animation update rate