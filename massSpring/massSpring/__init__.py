from gym.envs.registration import register 

register(
    id='massSpring-v0',
    entry_point='massSpring.envs:massSpringEnv',
)