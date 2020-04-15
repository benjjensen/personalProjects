import sys
sys.path.append('..')
import numpy as np

############## SIMULATION PARAMETERS ##################

ts_simulation = 0.01 # smallest time step for simulation
start_time = 0.  # start time for simulation
end_time = 50.  # end time for simulation

ts_plotting = 0.5  # refresh rate for plots

ts_video = 0.1  # write rate for video

ts_control = ts_simulation  # sample rate for the controller
 

###### WIND PARAMETERS %%%%%%%%%
wind_steadyState = np.array([np.random.randint(0,3), np.random.randint(0,3), np.random.randint(0,3)])
# wind_steadyState = np.array([0.0, 0.0, 0.0]) 