import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
from itertools import chain
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pdb
import massSpring
import time
import cv2 
import glob
from VideoWriter import videoWriter

PATH = "C:/Users/benjj/model.pth"

# env = gym.make('massSpring-v0')
# env.reset()
# env.render()
# env.close()


def get_action_dqn(network, state, epsilon, epsilon_decay, action_size):
  """Select action according to e-greedy policy and decay epsilon

    Args:
        network (QNetwork): Q-Network
        state (np-array): current state, size (state_size)
        epsilon (float): probability of choosing a random action
        epsilon_decay (float): amount by which to decay epsilon

    Returns:
        action (int): chosen action [0, action_size)
        epsilon (float): decayed epsilon
  """

  state = torch.from_numpy(state).float()
  if random.random() < epsilon:
      action = random.randint(0, action_size-1)  ### ### ###
  else:
      with torch.no_grad():
          action = torch.argmax(network(state)).item()

  epsilon *= epsilon_decay

  return action, epsilon

def prepare_batch(memory, batch_size):
  """Randomly sample batch from memory
     Prepare cuda tensors

    Args:
        memory (list): state, action, next_state, reward, done tuples
        batch_size (int): amount of memory to sample into a batch

    Returns:
        state (tensor): float cuda tensor of size (batch_size x state_size)
        action (tensor): long tensor of size (batch_size)
        next_state (tensor): float cuda tensor of size (batch_size x state_size)
        reward (tensor): float cuda tensor of size (batch_size)
        done (tensor): float cuda tensor of size (batch_size)
  """

  randBatch = random.randint(0, len(memory)-1)

  state = ([memory[randBatch][0]])
  action = ([memory[randBatch][1]])
  next_state = ([memory[randBatch][2]])
  reward = ([memory[randBatch][3]])
  done = ([float(memory[randBatch][4])])

  for batch in range(0, batch_size-1):
    randBatch = random.randint(0, len(memory)-1)
    state = np.append(state, [memory[randBatch][0]], axis = 0)
    action = np.append(action, [memory[randBatch][1]], axis = 0)
    next_state = np.append(next_state, [memory[randBatch][2]], axis = 0)
    reward = np.append(reward, [memory[randBatch][3]], axis = 0)
    done = np.append(done, [float(memory[randBatch][4])], axis = 0)

  state = torch.tensor(state, requires_grad = True).float()
  action = torch.tensor(action).long()   
  next_state = torch.tensor(next_state, requires_grad = True).float()
  reward = torch.tensor(reward, requires_grad = True).float()
  done = torch.tensor(done, requires_grad = True).float()    
  
  return state, action, next_state, reward, done

def learn_dqn(batch, optim, q_network, target_network, gamma, global_step, target_update):
  """Update Q-Network according to DQN Loss function
     Update Target Network every target_update global steps

    Args:
        batch (tuple): tuple of state, action, next_state, reward, and done tensors
        optim (Adam): Q-Network optimizer
        q_network (QNetwork): Q-Network
        target_network (QNetwork): Target Q-Network
        gamma (float): discount factor
        global_step (int): total steps taken in environment
        target_update (int): frequency of target network update
  """
  optim.zero_grad()

  batch_size = len(batch[1])
  states, actions, next_states, rewards, dones = batch[0], batch[1], batch[2], batch[3], batch[4]
  q_values = q_network.forward(states).gather(1, actions.view(-1,1)).squeeze()   # or q_network(states)...?
 
  target_q_values = target_network.forward(next_states) 

  future_values = (rewards + gamma*torch.max(target_q_values, 1)[0]*(1 - dones))

  objective = nn.MSELoss()
  loss = objective(q_values, future_values)

  loss.backward()    
  optim.step()
  if global_step % target_update == 0:
    target_network.load_state_dict(q_network.state_dict())

# Q-Value Network
class QNetwork(nn.Module):
  def __init__(self, state_size, action_size):
    super().__init__()
    hidden_size = 8
    
    self.net = nn.Sequential(nn.Linear(state_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, action_size))  
    
  def forward(self, x):
    """Estimate q-values given state

      Args:
          state (tensor): current state, size (batch x state_size)

      Returns:
          q-values (tensor): estimated q-values, size (batch x action_size)
    """
    
    return self.net(x)

def dqn_main():
  save_count = 1

  # Hyper parameters
  lr = 1e-3
  epochs = 1000
  start_training = 1000
  gamma = 0.99
  batch_size = 32
  epsilon = 1
  epsilon_decay = .99999
  target_update = 1000
  learn_frequency = 2

  # Init environment
  state_size = 4
  action_size = 3
  env = gym.make('massSpring-v0')

  # Init networks
  q_network = QNetwork(state_size, action_size)
  # q_network = torch.load(PATH)
  target_network = QNetwork(state_size, action_size)
  target_network.load_state_dict(q_network.state_dict())

  # Init optimizer
  optim = torch.optim.Adam(q_network.parameters(), lr=lr)

  # Init replay buffer
  memory = []

  saveVideo = False
  sim_time = 0.0

  # Begin main loop
  results_dqn = []
  global_step = 0
  loop = tqdm(total=epochs, position=0, leave=False)
  for epoch in range(epochs):
    last_epoch = (epoch+1 == epochs)
    if epoch % 200 == 199:
      video = videoWriter(video_name="massSpring.avi",
                      bounding_box=(100, 100, 1000, 1000),
                      output_rate=0.1)
      saveVideo = True
    # Reset environment
    state = env.reset()
    done = False
    cum_reward = 0  # Track cumulative reward per episode

    # Begin episode
    while not done: # and cum_reward < 10.:  # End after 200 steps 
      # Select e-greedy action
      action, epsilon = get_action_dqn(q_network, state, epsilon, epsilon_decay, action_size)

      # Take step
      next_state, reward, done, _ = env.step(action)
      if epoch % 100 == 99:
        env.render()

      if saveVideo:
        video.update(sim_time)
        sim_time += 0.01

      # Store step in replay buffer
      memory.append((state, action, next_state, reward, done))

      cum_reward += reward
      
      global_step += 1  # Increment total steps
      state = next_state  # Set current state

      # If time to train
      if global_step > start_training and global_step % learn_frequency == 0:

        # Sample batch
        batch = prepare_batch(memory, batch_size)
        
        # Train
        learn_dqn(batch, optim, q_network, target_network, gamma, global_step, target_update)
    ######################
    if epoch % 100 == 99:
      env.close()

    if saveVideo:
      saveVideo = False
      video.close()
    ######################
    # Print results at end of episode
    results_dqn.append(cum_reward)
    loop.update(1)
    loop.set_description('Episodes: {} Reward: {}'.format(epoch, cum_reward))
  
  # torch.save(q_network, PATH) #, "C:/Users/benjj/")
  return results_dqn

results_dqn = dqn_main()
plt.plot(results_dqn)
plt.show()


