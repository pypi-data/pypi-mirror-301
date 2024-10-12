import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
import pickle

import torch
import torch.nn.functional as F

from rllibs.rltorch import rl_utils

class PolicyNet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(PolicyNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return F.softmax(self.fc2(x), dim=1)
    
    
class ValueNet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim):
        super(ValueNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, 1)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)


class ActorCritic:
    def __init__(self, state_dim, hidden_dim, action_dim, actor_lr, critic_lr, gamma, device):
        self.actor = PolicyNet(state_dim, hidden_dim, action_dim).to(device)
        self.critic = ValueNet(state_dim, hidden_dim).to(device)  # 价值网络
        
        self.actor_optimizer  = torch.optim.Adam(self.actor.parameters(), lr=actor_lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=critic_lr)
        
        self.gamma = gamma
        self.device = device
        
    def take_action(self, state):
        state = torch.tensor([state], dtype=torch.float).to(self.device)
        probs = self.actor(state)  # 根据状态获取行动概率
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        return action.item()
    
    
    def update(self, transition_dict):
        import os
        # os.makedirs(f'/tmp/rl/ac/{NOW}', exist_ok=True)
        # with open(f'/tmp/rl/ac/{NOW}/transition_dict', 'wb') as transd: pickle.dump(transition_dict, transd)
        states      = torch.tensor(transition_dict['states'],      dtype=torch.float).to(self.device)
        next_states = torch.tensor(transition_dict['next_states'], dtype=torch.float).to(self.device)
        rewards     = torch.tensor(transition_dict['rewards'],     dtype=torch.float).view(-1, 1).to(self.device)
        dones       = torch.tensor(transition_dict['dones'],       dtype=torch.float).view(-1, 1).to(self.device)
        actions     = torch.tensor(transition_dict['actions']).view(-1, 1).to(self.device)
        
        # 时序差分 & 时序差分误差
        td_target = rewards + self.gamma * self.critic(next_states) * (1 - dones)
        td_delta = td_target - self.critic(states)
        
        log_probs = torch.log(self.actor(states).gather(1, actions))  # 在state下，采取actions的概率
        actor_loss = torch.mean(-log_probs * td_delta.detach())       # actor的loss
        
        # 均方误差
        critic_loss = torch.mean(F.mse_loss(self.critic(states), td_target.detach()))  # critic的loss
        
        self.actor_optimizer.zero_grad()
        self.critic_optimizer.zero_grad()
        actor_loss.backward()
        critic_loss.backward()
        self.actor_optimizer.step()
        self.critic_optimizer.step()

def main():
    actor_lr     = 1e-3
    critic_lr    = 1e-2
    num_episodes = 1000
    hidden_dim   = 128
    gamma = 0.98
    device = torch.device('cude') if torch.cuda.is_available() else torch.device('cpu')

    env_name = 'CartPole-v0'
    env = gym.make(env_name)
    env.reset()
    torch.manual_seed(0)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    agent = ActorCritic(state_dim, hidden_dim, action_dim, actor_lr, critic_lr, gamma, device)
    return_list = rl_utils.train_on_policy_agent(env, agent, num_episodes)
    return return_list



if __name__ == '__main__':
    main()