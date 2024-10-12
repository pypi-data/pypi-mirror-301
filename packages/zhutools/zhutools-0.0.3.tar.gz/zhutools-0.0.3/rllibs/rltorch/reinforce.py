import torch
import torch.nn.functional as F
import gymnasium as gym

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from rllibs.rltorch import rl_utils

class PolicyNet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(PolicyNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return F.softmax(self.fc2(x), dim=1)
    
    
class REINFORCE:
    def __init__(self, state_dim, hidden_dim, action_dim, learning_rate, gamma, device):
        self.policy_net = PolicyNet(state_dim, hidden_dim, action_dim).to(device)
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=learning_rate)  # 使用adam优化器
        self.gamma = gamma
        self.device = device
        
    def take_action(self, state):  # 根据动作概率分布随机采样
        state = torch.tensor([state], dtype=torch.float).to(self.device)
        probs = self.policy_net(state)
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        return action.item()
    
    def update(self, transition_dict):
        reward_list = transition_dict['rewards']
        state_list  = transition_dict['states']
        action_list = transition_dict['actions']
        
        G = 0
        self.optimizer.zero_grad()
        for i in reversed(range(len(reward_list))):  # 从最后一步算起
            reward   = reward_list[i]
            state    = torch.tensor([state_list[i]], dtype=torch.float).to(self.device)
            action   = torch.tensor([action_list[i]]).view(-1, 1).to(self.device)
            log_prob = torch.log(self.policy_net(state).gather(1, action))  # 获得Q(s, a)
            
            G = self.gamma * G + reward
            loss = - log_prob * G
            loss.backward()
        self.optimizer.step()

def main():
    learning_rate = 1e-3
    num_episodes = 1000
    hidden_dim = 128
    gamma = 0.98

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    env_name = "CartPole-v0"
    env = gym.make(env_name)
    torch.manual_seed(0)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = REINFORCE(state_dim, hidden_dim, action_dim, learning_rate, gamma, device)

    return_list = rl_utils.train_on_policy_agent(env, agent, num_episodes)



if __name__ == '__main__':
    main()