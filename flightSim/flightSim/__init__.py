from gym.envs.registration import register 

register(
    id='flightSim-v0',
    entry_point='flightSim.envs:flightSimEnv'
)