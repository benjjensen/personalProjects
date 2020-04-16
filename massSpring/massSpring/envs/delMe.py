import gym

env = gym.make('CartPole-v0')
env.reset()
env.render()
pause(1.)
env.close()