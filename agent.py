import numpy as np
import random

from param import ext_state_vars, ext_state_space, int_state_space, action_space, alpha, gamma, epsilon

## TODO:
## 1. q table monitoring
## 2. private and static methods

## 3. param bounds and time variants
## 4. Diff Algos: Inheritance and Polymorphism

class Agent():# Expected SARSA (On-policy implementation)
    def __init__(self):
        self.state_space = len(ext_state_space) * len(int_state_space)
        self.action_space = len(action_space)
        self.q_table = np.random.rand(self.state_space, self.action_space)
        
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
    
    def get_state(self, int_state, ext_states):
        return int_state << len(ext_state_vars) + ext_states

    def greedy_action_selection(self, state):
        q_max = (np.argmax(q_table[state, :])).reshape(-1)
        action = np.random.choice(q_max)
        return action

    def action_probs(self, state):# epsilon-greedy
        best_action = self.greedy_action_selection(state)
        probas = self.epsilon / self.action_space * np.ones(self.action_space)
        probas[best_action] += (1.0 - self.epsilon)
        return probas

    def take_action(self, int_state, ext_states):# epsilon-greedy
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_space)
        else:
            return self.greedy_action_selection(self.get_state(int_state, ext_states))

    def learn(self, int_state_old, ext_states_old, int_state_new, ext_states_new, action_old, reward):
        state_old = self.get_state(int_state_old, ext_states_old)
        state_new = self.get_state(int_state_new, ext_states_new)

        state_new_probs = self.action_probs(state_new).reshape(-1)
        state_new_q_val = (self.q_table[state_new, :]).reshape(-1)
        state_new_expct = np.sum(state_new_probs * state_new_q_val)

        delta = self.alpha * (reward + self.gamma * state_new_expct - self.q_table[state_old, action_old])
        self.q_table[state_old, action_old] += delta