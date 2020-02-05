# https://scipython.com/blog/the-double-pendulum/

''' To Do 
- Move to Github
- Clean up
- Make trails?
- Speed it up
'''

import matplotlib.pyplot as plt 
import numpy as np 
import sys
sys.path.append('..')
import Parameters as P 
from Animation import Animation
from Dynamics import Dynamics
from signalGenerator import signalGenerator
import glob
import moviepy.editor as mpy

gif_name = 'doublePendulum'
fpsFast = 30

# Generate the images
animation = Animation()
dynamics = Dynamics()

t = P.t_start
z = dynamics.states()
while t < P.t_end:

    dynamics.propagateDynamics(0.0)
    t = t + P.Ts
    state = dynamics.states()

    animation.drawSystem(state)
    plt.pause(0.0001)

# Make the Gif
file_list = glob.glob("C:/Users/benjj/Documents/College/gifs/*.png")
list.sort(file_list, key = lambda x: int(x.split('_')[1].split('.png')[0]))
clip = mpy.ImageSequenceClip(file_list, fps = fpsFast) 
clip.write_gif('{}.gif'.format(gif_name), fps=fpsFast)

plt.close()