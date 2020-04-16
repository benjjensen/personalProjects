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

# env = gym.make('massSpring-v0')
# env.reset()
# env.render()
# env.close()

def calculate_return(memory, rollout, gamma):
  """Return memory with calculated return in experience tuple

    Args:
        memory (list): (state, action, action_dist, return) tuples
        rollout (list): (state, action, action_dist, reward) tuples from last rollout
        gamma (float): discount factor

    Returns:
        list: memory updated with (state, action, action_dist, return) tuples from rollout
  """
  ret = 0
  length = len(rollout)

  # reverse rollout, get state, action, action_dist, and reward
  for tupl in range(0, length):
    state, action, action_dist, reward = rollout[-tupl][0], rollout[-tupl][1], rollout[-tupl][2], rollout[-tupl][3]
    ret = reward + ret * gamma 
    memory.append(( state, action, action_dist, ret)) # randomly sampled, order doesn't matter

  return memory

def get_action_ppo(network, state):
  """Sample action from the distribution obtained from the policy network

    Args:
        network (PolicyNetwork): Policy Network
        state (np-array): current state, size (state_size)

    Returns:
        int: action sampled from output distribution of policy network
        array: output distribution of policy network
  """
  state = torch.from_numpy(state).unsqueeze(0).float()
  with torch.no_grad():
    action_dist = network(state)
    action = torch.multinomial(action_dist, 1)  # gather one sample from the action_dist
    return action.cpu().numpy().item(), action_dist.cpu().numpy() # convert back to np arrays first

def learn_ppo(optim, policy, value, memory_dataloader, epsilon, policy_epochs):
  """Implement PPO policy and value network updates. Iterate over your entire 
     memory the number of times indicated by policy_epochs.    

    Args:
        optim (Adam): value and policy optimizer
        policy (PolicyNetwork): Policy Network
        value (ValueNetwork): Value Network
        memory_dataloader (DataLoader): dataloader with (state, action, action_dist, return) tensors
        epsilon (float): trust region
        policy_epochs (int): number of times to iterate over all memory
  """
  objective = nn.MSELoss()

  for i in range(0, policy_epochs):
    for state, action, action_dist, ret in memory_dataloader:
      optim.zero_grad()
      state, action, action_dist, ret = state.float().squeeze(), action, action_dist, ret

      ## Value loss
      valueLoss = objective(ret, value(state).squeeze())


      ## Policy Loss

      # advantage, remembering to detach
      advantage = (ret - value(state).squeeze()).detach()

      # ratio
      new_action_dist = policy(state)
      old_action_dist = action_dist

      num = new_action_dist.gather(1, action.view(-1,1)).squeeze()
      den = old_action_dist.squeeze().gather(1, action.view(-1,1)).squeeze()

      policy_action_ratio = num/den

      ratio = torch.min(policy_action_ratio*advantage, torch.clamp(policy_action_ratio, 1-epsilon, 1+epsilon)*advantage)
      policyLoss = -torch.mean(ratio)

      ## Total Loss
      totalLoss = valueLoss + policyLoss
      totalLoss.backward()
      optim.step()

    # Add loss functions and backprop, optim.step and .zero_grad()

# Dataset that wraps memory for a dataloader
class RLDataset(Dataset):
  def __init__(self, data):
    super().__init__()
    self.data = []
    for d in data:
      self.data.append(d)
  
  def __getitem__(self, index):
    return self.data[index]
 
  def __len__(self):
    return len(self.data)

# Policy Network
class PolicyNetwork(nn.Module):
  def __init__(self, state_size, action_size):
    super().__init__()
    hidden_size = 8
    
    self.net = nn.Sequential(nn.Linear(state_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, action_size),
                             nn.Softmax(dim=1))
  
  def forward(self, x):
    """Get policy from state

      Args:
          state (tensor): current state, size (batch x state_size)

      Returns:
          action_dist (tensor): probability distribution over actions (batch x action_size)
    """
    return self.net(x)
  
# Value Network
class ValueNetwork(nn.Module):
  def __init__(self, state_size):
    super().__init__()
    hidden_size = 8
  
    self.net = nn.Sequential(nn.Linear(state_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, hidden_size),
                             nn.ReLU(),
                             nn.Linear(hidden_size, 1))
    
  def forward(self, x):
    """Estimate value given state

      Args:
          state (tensor): current state, size (batch x state_size)

      Returns:
          value (tensor): estimated value, size (batch)
    """
    return self.net(x)

def ppo_main():
  # Hyper parameters
  lr = 1e-3
  epochs = 40
  env_samples = 100
  gamma = 0.9
  batch_size = 256
  epsilon = 0.2
  policy_epochs = 5

  # Init environment 
  state_size = 4
  action_size = 3
  env = gym.make('massSpring-v0')

  # Init networks
  policy_network = PolicyNetwork(state_size, action_size)
  value_network = ValueNetwork(state_size)

  # Init optimizer
  optim = torch.optim.Adam(chain(policy_network.parameters(), value_network.parameters()), lr=lr)

  # Start main loop
  results_ppo = []
  loop = tqdm(total=epochs, position=0, leave=False)
  for epoch in range(epochs):
    
    memory = []  # Reset memory every epoch
    rewards = []  # Calculate average episodic reward per epoch

    # Begin experience loop
    for episode in range(env_samples):
      
      # Reset environment
      state = env.reset()
      done = False
      rollout = []
      cum_reward = 0  # Track cumulative reward

      # Begin episode
      while not done: # and cum_reward < 200:  # End after 200 steps   
        # Get action
        action, action_dist = get_action_ppo(policy_network, state)
        
        # Take step
        next_state, reward, done, _ = env.step(action)
        
        if (epoch % 10 == 0) & (episode == 0):
            env.render()

        # Store step
        rollout.append((state, action, action_dist, reward))

        cum_reward += reward
        state = next_state  # Set current state

      # Calculate returns and add episode to memory
      memory = calculate_return(memory, rollout, gamma)

      rewards.append(cum_reward)
      ######################
      if (epoch % 10 == 0) and (episode == 0):
          env.close()
      ######################
    # Train
    dataset = RLDataset(memory)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    learn_ppo(optim, policy_network, value_network, loader, epsilon, policy_epochs)
    
    # Print results
    results_ppo.extend(rewards)  # Store rewards for this epoch
    loop.update(1)
    loop.set_description("Epochs: {} Reward: {}".format(epoch, results_ppo[-1]))

  return results_ppo

results_ppo = ppo_main()
