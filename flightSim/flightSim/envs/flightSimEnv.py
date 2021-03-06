import gym
from gym import error, spaces, utils
from gym.utils import seeding 
import numpy as np 

# from flightSim.envs.NAME import NAME
from flightSim.envs.Animation import spacecraft_animator 
from flightSim.envs.mav_dynamics4 import mav_dynamics 
from flightSim.envs.wind_simulation import wind_simulation 
from flightSim.envs.autopilot import autopilot 
from flightSim.envs.tools.signals import signals
# from flightSim.envs.trim import compute_trim 
from flightSim.envs.msg_autopilot import msg_autopilot 
from flightSim.envs import aerosonde_parameters as MAV
# from flightSim.envs.data_viewer import data_viewer

from matplotlib import pyplot as plt

class flightSimEnv(gym.Env):
    '''
    Description:
        A flight simulator is created, with four controls (throttle, aileron, elevator, rudder)
        A force is applied to ONE (for now) of the four controls to steer plane to a specified location.

    State:
        Type: Box(15) 
        Num     Observation         Min     Max 
        0       Position (north)
        1       Position (east)
        2       Position (down)
        3       U
        4       V
        5       W 
        6       Quaternion E0
        7       Quaternion E1
        8       Quaternion E2
        9       Quaternion E3
        10      P
        11      Q
        12      R
        13      Commanded Position 
        14      Current Force

    Actions:
        Type: Discrete(3) 
        Num     Action
        0       Increase force (negative)
        1       Do nothing
        2       Increase force (positive)

    Reward:
        Reward is -1 * error from commanded position
                    - OR - 
        Reward is TODO 'SOME LARGE VALUE' for being close

    Starting State:

    Episode Termination:
        Cumulative Error surpasses a threshold
    '''

    metadata = {'render.modes': ['human','rgb_array']}

    def __init__(self):
        ''' Sets initial environment state'''
        self.forceFactor = .02      # Factor to scale force
        self.totalForce = 0.0       # Tracks total force being currently applied
        self.error = 0.0            # Tracks total error for round
        self.maxError = 50000.0     # Limit for error before termination

        self.thresholds = np.array([np.infty, np.infty, np.infty, np.infty, np.infty, np.infty, \
                                        np.infty, np.infty, np.infty, np.infty, np.infty, np.infty, \
                                        np.infty, np.infty]) # TODO Is this even useful now?
        self.action_space = spaces.Discrete(3) 
        self.observation_space = spaces.Box(-self.thresholds, self.thresholds)

        self.seed()

        self.state = None # [pn, pe, pd, u, v, w, e0, e1, e2, e3, p, q, r] + command, current angle
        self.viewer = None # TODO ---- Do I want this...?
        self.steps_beyond_done = None
        # self.data_view = data_viewer()

        self.timeStep = 0.01 
        self.currentTime = 0.0

        self.dynamics = mav_dynamics(self.timeStep) # TODO 
        self.mav_view = spacecraft_animator() 
        self.wind = wind_simulation(self.timeStep)
        self.ctrl = autopilot(self.timeStep)
        self.commands = msg_autopilot()
        self.Va_command = signals(dc_offset=25.0, amplitude=3.0, start_time=10.0, frequency = 0.001) # TODO 
        self.h_command = signals(dc_offset=100.0, amplitude=10.0, start_time=0.0, frequency = 0.05)
        self.chi_command = signals(dc_offset=np.radians(180), amplitude=np.radians(1), start_time=10.0, frequency = 0.1)

        self.renderFlag = False
        self.elevator_command = -0.2

        self.totalCount = 0.0

    def seed(self, seed = None):
        ''' Seeds random '''
        self.np_random, seed = seeding.np_random(seed)
        return [seed] 

    def step(self, action):
        '''
            Takes in an action, runs it through dynamics, and returns a list of:
            - Next State
            - Reward for current state 
            - Boolean 'done'
            - (other)
        '''
        ''' ---------- CONTROLLER ---------- '''
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        tempState = self.dynamics.msg_true_state
        self.commands.airspeed_command = 25.0 # TODO ? 
        self.commands.course_command = self.chi_command.square(self.currentTime) # 0.0 # TODO ? 
        self.commands.altitude_command = 100 # self.h_command.square(self.currentTime)
        delta, commanded_state = self.ctrl.update(self.commands, tempState) #TODO update to take in only one?
        old_elevator = delta[1]

        # TODO Verify 
        self.elevator_command += self.forceFactor * (action - 1.0) # -1 sets action to range -1 -> 1 * forceFactor (0.02?)
        delta[1] = self.elevator_command 

        ''' ---------- PHYSICAL SYSTEM ---------- '''
        current_wind = np.array([[0.0], [0.0], [0.0],[0.0], [0.0], [0.0]]) #self.wind.update()       # Set to always be 0 
        self.dynamics.update_state(delta, current_wind) 

        self.currentTime += self.timeStep

        releventCommand = self.commands.altitude_command
        self.error += np.absolute(releventCommand - tempState.h)   # Shound this include other error, too?
        done = bool((self.error > self.maxError))

        tempState = self.dynamics._state
        self.state = np.array([ [tempState[2]], # pd
                                [tempState[4]], # v
                                [tempState[11]] ])  # q                 ADD IN ERROR?
        self.state = np.append(self.state, releventCommand)
        self.state = np.append(self.state, delta[1]) # 

        ''' ---------- REWARD ---------- '''
        if done and (self.steps_beyond_done is None):
            self.steps_beyond_done = 0.
        elif done: 
            print("Error! Calling step() after already done")
        
        reward = np.absolute(releventCommand + self.state[0]) * -1 # TODO 
        if (reward > -1.):
            reward = 500. # 300 & 30 
        elif (reward > -10.):
            reward = 100.

        if  (np.abs(delta[0]) > np.radians(45)) \
            or (np.abs(delta[1]) > np.radians(45)) \
            or (np.abs(delta[2]) > np.radians(45)):
            reward = -1000.

        return self.state, reward, done, {} 

    def newStep(self, action):
        '''
            Takes in an action, runs it through dynamics, and returns a list of:
            - Next State
            - Reward for current state 
            - Boolean 'done'
            - (other)
        '''
        ''' ---------- CONTROLLER ---------- '''
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        tempState = self.dynamics.msg_true_state
        self.commands.airspeed_command = 25.0 # TODO ? 
        self.commands.course_command = 0.0 # TODO ? 
        self.commands.altitude_command = self.h_command.square(self.currentTime)
        delta, self.commanded_state = self.ctrl.update(self.commands, tempState) #TODO update to take in only one?

        # delta[0:4] = Rudder, Elevator, Aileron, Throttle
        old_elevator = delta[1]

        # TODO Verify 
        self.elevator_command += self.forceFactor * (action - 1.0) # -1 sets action to range -1 -> 1 * forceFactor (0.02?)
        delta[1] = self.elevator_command 

        ''' ---------- PHYSICAL SYSTEM ---------- '''
        current_wind = np.array([[0.0], [0.0], [0.0],[0.0], [0.0], [0.0]]) #self.wind.update()       # Set to always be 0 
        self.dynamics.update_state(delta, current_wind) 

        self.currentTime += self.timeStep

        releventCommand = self.commands.altitude_command
        tempState = self.dynamics._state
        self.state = np.array([ [tempState[2]], # pd
                                [tempState[4]], # v
                                [tempState[11]] ])  # q
        self.state = np.append(self.state, releventCommand)
        self.state = np.append(self.state, delta[1]) # self.totalForce)

        # error = np.absolute(releventCommand + self.state[2])
        error = np.absolute(releventCommand + self.state[0])

        ''' ---------- TERMINATION --------- '''
        done = (np.abs(delta[0]) > np.radians(45)) \
                or (np.abs(delta[1]) > np.radians(45)) \
                or (np.abs(delta[2]) > np.radians(45)) \
                or error > 50.0
        done = bool(done)

        ''' ---------- REWARD ---------- '''
        if done and (self.steps_beyond_done is None):
            self.steps_beyond_done = 0.
        elif done: 
            print("Error! Calling step() after already done")
        
        reward = 50 - error # 1.0
        if (np.absolute(releventCommand + self.state[0]) < 5): ###
            reward = 300.0
        elif (np.absolute(releventCommand + self.state[0]) < 8): ###
            reward = 75.0

        return self.state, reward, done, {} 

    def reset(self):
        ''' Resets state in preparation for a new round '''
        self.steps_beyond_done = None 
        self.currentTime = 0.0 
        self.totalForce = 0.0 
        self.error = 0.0 
        self.elevator_command = -0.2
        self.dynamics.reset()  
        self.totalCount += 1

        # if self.totalCount == 500:
        #     print("Total Count is 500")
        # self.state = np.array([[MAV.pn0],  # (0)
        #                 [MAV.pe0],   # (1)
        #                 [MAV.pd0],   # (2)
        #                 [MAV.u0],    # (3)
        #                 [MAV.v0],    # (4)
        #                 [MAV.w0],    # (5)
        #                 [MAV.e0],    # (6)
        #                 [MAV.e1],    # (7)
        #                 [MAV.e2],    # (8)
        #                 [MAV.e3],    # (9)
        #                 [MAV.p0],    # (10)
        #                 [MAV.q0],    # (11)
        #                 [MAV.r0]])

        self.state = np.array([ [MAV.pd0], 
                                [MAV.v0],
                                [MAV.q0] ])

        self.state = np.append(self.state, self.h_command.square(self.currentTime))
        self.state = np.append(self.state, self.elevator_command) #self.totalForce)                        
        return self.state

    def render(self, mode='human'):
        # if self.renderFlag:
        #     self.mav_view = spacecraft_animator() 
        self.mav_view.update(self.dynamics.msg_true_state)

        # self.data_view.update(self.dynamics.msg_true_state, # true states
        #              self.dynamics.mav.msg_true_state, # estimated states
        #              self.commanded_state, # commanded states
        #              0.01)
        
    def close(self):
        ''' Closes the rendering window '''
        if self.viewer:
            self.viewer.close() 
            self.viewer = None

'''
    To Try:
    - Only return some of the values, instead of all
    - Include error in other areas, too
    - verify efficacy of sim6
    - Need plots....
    - Mess with the box bounds
    randomize starting

    2) Work on new reward:
        Positive:       <- Better 
            - +1 point for being alive (+20 for being on command?)
            - Terminate if:
                - Row or pitch are too extreme
                - Too far from command
        Negative:
            - -1 per error - 1 * row angle?
'''
        

