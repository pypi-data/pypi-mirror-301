import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from numpy.random import default_rng

__rng__ = default_rng()

def __compute_discounted_rewards__(rewards, gamma, device):
    cum_rewards = torch.zeros((rewards.shape[0])).to(device)
    reward_len = len(rewards)
    for j in reversed(range(reward_len)):
        cum_rewards[j] = rewards[j] + (cum_rewards[j+1]*gamma if j+1 < reward_len else 0)
    return cum_rewards

def __get_out_features__(model:nn.Module) -> int:
    out_features = 0
    for layer in model.children():
        if hasattr(layer, 'out_features'):
            out_features = layer.out_features
    return out_features

class ExperienceReplayMemory():
    def __init__(self, size:int, sdim:int):
        self.size = size
        
        self.states = torch.zeros((size, sdim))
        self.actions = torch.zeros((size))
        self.rewards = torch.zeros((size))
        self.next_states = torch.zeros((size, sdim))
        self.dones = torch.zeros((size))

        self.len = 0
        self.i = 0

    def append(self, state:torch.Tensor, action:int, reward:float, next_state:torch.Tensor, done:bool):
        self.states[self.i] = state
        self.actions[self.i] = action
        self.rewards[self.i] = reward
        self.next_states[self.i] = next_state
        self.dones[self.i] = done

        if self.i < self.size - 1:
            self.i += 1
        else:
            self.i = 0

        if self.len < self.size - 1:
            self.len += 1

    def sample(self, batch_size:int):
        if self.len < batch_size:
            return None, None, None, None, None
        indices = __rng__.choice(self.len, size=batch_size, replace=False)
        states = self.states[indices]
        actions = self.actions[indices]
        rewards = self.rewards[indices]
        next_states = self.next_states[indices]
        dones = self.dones[indices]

        return states, actions, rewards, next_states, dones

class Agent():
    def __init__(self):
        pass

    def act(self, state:torch.Tensor) -> int:
        raise NotImplementedError()

class A2CAgent(Agent):
    def __init__(self, sdim:int, adim:int, hdim:int = 16, gamma = 0.99, lr:float = 0.001,
                 actor_model = None, critic_model = None, device = 'cpu'):
        super(A2CAgent, self).__init__()
        self.gamma = gamma

        self.device = device

        if actor_model is not None:
            self.actor = actor_model
        else:
            self.actor = nn.Sequential(
                nn.Linear(sdim, hdim),
                nn.ReLU(),
                nn.Linear(hdim, adim)
            )
        
        if critic_model is not None:
            self.critic = critic_model
        else:
            self.critic = nn.Sequential(
                nn.Linear(sdim, hdim),
                nn.ReLU(),
                nn.Linear(hdim, 1)
            )

        self.actor.to(device)
        self.critic.to(device)

        self.opt_actor = torch.optim.Adam(self.actor.parameters(), lr=lr)
        self.opt_critic = torch.optim.Adam(self.critic.parameters(), lr=lr)

    def act(self, state):
        with torch.no_grad():
            logits = self.actor(state)
        probs = F.softmax(logits, dim=1)
        action = torch.multinomial(probs, num_samples=1)[0].item()
        return action
    
    def train(self, states, actions, rewards):
        states = torch.stack(states).squeeze(1)
        rewards = torch.tensor(rewards)

        # critic loss
        self.opt_critic.zero_grad()
        discounted_rewards = __compute_discounted_rewards__(rewards, self.gamma, self.device)
        values = self.critic(states).squeeze(1)
        critic_loss = F.mse_loss(values, discounted_rewards, reduction='none')
        critic_loss.sum().backward()
        self.opt_critic.step()

        # actor loss
        self.opt_actor.zero_grad()
        with torch.no_grad():
            values = self.critic(states).squeeze(1)
        actions = torch.tensor(actions).to(self.device)
        advantages = discounted_rewards - values
        logits = self.actor(states)
        log_probs = -F.cross_entropy(logits, actions, reduction='none')
        actor_loss = -log_probs * advantages
        actor_loss.sum().backward()
        self.opt_actor.step()
        
        return actor_loss.sum().item(), critic_loss.sum().item(), rewards.sum().item()

class QLearningAgent(Agent):
    def __init__(
            self,
            model:nn.Module = None,
            sdim:int = None,
            adim:int = None,
            buffer_size:int = 1000
        ):
        super(QLearningAgent, self).__init__()

        if model is None and (sdim is None or adim is None):
            raise Exception(f'Please provide model or sdim and adim.')

        if model is None:
            self.model = nn.Sequential(
                nn.Linear(sdim, 32),
                nn.ReLU(),
                nn.Linear(32, 32),
                nn.ReLU(),
                nn.Linear(32, adim)
            )
            self.adim = adim
        else:
            self.model = model
            self.adim = __get_out_features__(self.model)

        self.buffer = ExperienceReplayMemory(buffer_size, sdim)

    def act(self, state:torch.Tensor, epsilon:float) -> int:
        self.model.eval()
        if np.random.random() > epsilon:
            with torch.no_grad():
                Y = self.model(state)
                action = torch.argmax(Y).item()
        else:
            action = np.random.randint(0, self.adim)

        return action

if __name__ == '__main__':
    EPOCHS = 10000
    BATCH_SIZE = 32

    from rsp.drl.environment.environment import GymCartPoleV1
    env = GymCartPoleV1()
    agent = QLearningAgent(sdim = env.state_dim, adim = env.action_dim)

    epoch = 0
    while epoch < EPOCHS:
        epsilon = 1 - (epoch / EPOCHS)

        state, reward, done = env.reset()

        while not done:
            action = agent.act(state, epsilon)

            next_state, reward, done = env.step(action)

            agent.buffer.append(state, action, reward, next_state, done)

            state = next_state.clone()

        agent.buffer.sample(BATCH_SIZE)

        epoch += 1