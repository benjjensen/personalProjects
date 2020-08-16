import gym
from gym import error, spaces, utils 
from gym.utils import seeding 
import numpy as np 
import math
from massSpring.envs.massSpringDynamics import MassSpringDynamics
from massSpring.envs.signalGenerator import SignalGenerator


class massSpringEnv(gym.Env):
    '''
    Description:
        A mass is attached by a spring to a wall. A force is applied, with the goal being to position
            the mass at a specified location

    State:
        Type:   Box(4)           <- allows an n-dimesional array
        Num     Observation         Min             Max
        0       Position            0.0             
        1       Velocity            -Inf            Inf  
        2       Commanded Position          
        3       Current Force 

    Actions:
        Type:   Discrete(3)       <- Allows a fixed range of non-negative numbers (0, 1, or 2)
        Num     Action
        0       Increase force left
        1       Do nothing
        2       Increase force right

    Reward: (punishment) 
        Reward is -1 * error (m) from commanded position
        If error is small, a large positve reward is used instead

    Starting State:
        
    Episode Termination:
        Episode Length is greater than XXXXX
    '''


    metadata = {'render.modes': ['human', 'rgb_array'] } # TODO: No idea what this means

    def __init__(self):
        ''' Sets initial State '''
        self.mass = 5.                      # Mass(kg)
        self.k = 4                          # Spring constant (N/m)
        self.len = 100.0                    # Length of spring (m)    TODO whaaa?
        self.b = 0.5                        # Damper coefficient (N*sec/m)
        self.forceFactor = 100.0            # Factor to scale the force (options are -1, 0, or 1 * this in newtons)
        self.len_threshold = 3. * self.len  # Locations at which to fail the episode TODO
        self.max_speed = np.infty           # TODO 

        self.minSpring_location = -100.0    # Left side of the spring
        self.max_position = np.array([np.infty, self.max_speed, np.infty, np.infty ], dtype = np.float32)

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(-self.max_position, self.max_position)      # TODO
        self.seed()

        self.defaultPosition = 0.0      # (m) 
        self.defaultVelocity = 0.0      # (m/s)

        self.state = None # Position, velocity, command, current force
        self.viewer = None
        self.steps_beyond_done = None   # Error detection - ensure we aren't calling step() after done

        self.commands = SignalGenerator(amplitude = 100.0, frequency = 0.07, y_offset = self.defaultPosition)

        self.timeStep = 0.01
        self.currentTime = 0.0
        self.refInput = self.commands.square(self.currentTime)[0]
        self.refInput_prev = self.refInput
        self.dynamics = MassSpringDynamics(self.mass, self.k, self.b, self.len, self.timeStep)
        self.maxTime = 3.0
        self.force = 0.0

        # Testing - 
        self.error = 0.0
        self.maxError = 100000.0
        self.totalReward = 0.0
        self.randomizerFactor = 1

    def seed(self, seed=None):
        ''' Seeds random '''
        self.np_random, seed = seeding.np_random(seed)
        return [seed]   # TODO is return necessary...?

    def step(self, action):
        ''' 
            Takes in an action, and returns list of:
            - Next state
            - Reward for current state
            - Boolean 'done' 
            - (other)
        '''
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        
        self.force += self.forceFactor * (action - 1.0) # -1 sets action to be (-1, 0, or 1)
        self.dynamics.propagateDynamics(self.force)
        self.state = self.dynamics.states()  # Only returns position, velocity
        self.refInput = self.commands.square(self.currentTime)[0] * self.randomizerFactor
        self.state = np.append(self.state, self.refInput)
        self.state = np.append(self.state, self.force)
        self.currentTime += self.timeStep # TODO is there a better way to do this?

        self.error += np.absolute(self.refInput - self.state[0]) 

        self.currentTime += self.timeStep
        done = (self.error > self.maxError) #or (self.totalReward > 30000.0)
        done = bool(done)

        if not done:
            reward = 1.0 # np.absolute(self.refInput - self.state[0]) * -0.1 # Reward proportional to error
        elif self.steps_beyond_done is None: # First time hitting done - Good!
            self.steps_beyond_done = 0
            reward = 0.0
        else:
            self.steps_beyond_done += 1
            print("Error! Calling step() after already done")
            reward = 1.0 # 0.0

        reward = np.absolute(self.refInput - self.state[0]) * -0.1 # Reward proportional to error

        if np.absolute(self.refInput - self.state[0]) < 1:
            reward = 500
        elif np.absolute(self.refInput - self.state[0]) < 10:
            reward = 30

        self.totalReward += reward

        return self.state, reward, done, {}

    def reset(self):
        ''' Resets the state '''
        self.steps_beyond_done = None
        self.currentTime = 0.0
        self.force = 0.0
        self.error = 0.0
        self.totalReward = 0.0
        self.dynamics.reset()
        self.refInput_prev = self.refInput
        self.state = np.array([self.np_random.uniform(low=-10., high=20.), self.defaultVelocity, self.refInput, self.np_random.uniform(low=-500., high = 500.)])

        # tempRandomizer = np.random.randint(0,2)
        # if tempRandomizer == 0:
        #     self.randomizerFactor = -1
        # else:
        #     self.randomizerFactor = 1

        return self.state

    def render(self, mode='human'): # , close=False):
        ''' Gives out relevent information '''
        screen_width = 600
        screen_height = 400 

        world_width = self.len_threshold * 2.0
        scale = screen_width / world_width 

        springwidth = 4.0 # 10.0
        masswidth = 60.0 # 50.0
        massheight = 35.0 # 30.0
        mass_y = 100.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering 
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # Make mass
            l, r, t, b = -masswidth/2., masswidth/2., massheight/2., -massheight/2.
            mass = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.masstrans = rendering.Transform() # does this allow it to move?
            mass.add_attr(self.masstrans)
            self.viewer.add_geom(mass)

            # Make spring
            l, r, t, b = self.minSpring_location, self.defaultPosition, springwidth/2., -springwidth/2.
            spring = rendering.FilledPolygon([ (l, b), (l, t), (r, t), (r, b)])
            spring.set_color(0.8, 0.6, 0.4)  # TODO eventually...
            self.springtrans = rendering.Transform()
            spring.add_attr(self.springtrans)
            spring.add_attr(self.masstrans) 
            self.viewer.add_geom(spring)

            # Make Track
            self.track = rendering.Line((0.0, mass_y-massheight/2.), (screen_width, mass_y-massheight/2.))
            self.track.set_color(0.0, 0.0, 1.0) #
            self.viewer.add_geom(self.track)
            
            l, r, t, b = (screen_width/2.0 + self.refInput - 30), (screen_width/2.0 + self.refInput + 30.), (mass_y - massheight/2.0 - 2.0), (mass_y - massheight/2.0 + 2.0)  
            self.command = rendering.FilledPolygon([ (l,b), (l,t), (r,t), (r,b)])
            self.command.set_color(1.0, 0.0, 0.0)
            self.viewer.add_geom(self.command)

            self._spring_geom = spring  # TODO Necessary?
            self._command_geom = self.command

        if self.state is None: return None

        # Update 
            # Mass
        x = self.state[0] # new position
        mass_x = x * scale + screen_width / 2.0 # middle of mass
        self.masstrans.set_translation(mass_x, mass_y)

        l, r, t, b = (screen_width/2.0 + self.refInput - 30), (screen_width/2.0 + self.refInput + 30.), (mass_y - massheight/2.0 - 2.0), (mass_y - massheight/2.0 + 2.0)  
        self._command_geom.v = [(l,b), (l,t), (r,t), (r,b)]

            # Spring
        l, r, t, b =-x, 0.0, springwidth/2., -springwidth/2.
        self._spring_geom.v = [(l,b), (l,t), (r,t), (r,b)]

        return self.viewer.render(return_rgb_array = mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close() 
            self.viewer = None

