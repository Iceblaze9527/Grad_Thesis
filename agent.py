import numpy as np
import random

## TODO:
## 1. q table monitoring
## 2. private and static methods

## 3. param bounds and time variants
## 4. Inheritance and Polymorphism

class Agent():
    def __init__(self, state_space, action_space, alpha = 0.5, gamma=0.9, epsilon = 0.1):
        self.action_space = action_space
        self.q_table = np.random.rand(state_space, action_space)
        
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def greedy_action_selection(self, state):
        q_max = (np.argmax(q_table[state, :])).reshape(-1)
        action = np.random.choice(q_max)
        return action

    def action_probs(self, state):# epsilon-greedy
        best_action = self.greedy_action_selection(state)
        probas = self.epsilon / self.action_space * np.ones(self.action_space)
        probas[best_action] += (1.0 - self.epsilon)
        return probas

    def take_action(self, state):# epsilon-greedy
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_space)
        else:
            return self.greedy_action_selection(state)

    def learn(self, state_old, state_new, action_old, reward):# Expected SARSA (On-policy implementation)
        state_new_probs = self.action_probs(state_new).reshape(-1)
        state_new_q_val = (self.q_table[state_new, :]).reshape(-1)
        state_new_expct = np.sum(state_new_probs * state_new_q_val)
        
        delta = self.alpha * (reward + self.gamma * state_new_expct - self.q_table[state_old, action_old])
        self.q_table[state_old, action_old] += delta