import numpy as np
import random

class Agent:
    def __init__(self, state_space, action_space, alpha = 0.5, gamma=0.9, epsilon = 0.1):
        self.q_table = []## Q-table (state_space, action_space) ##random assigned value (bounded)

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
    def get_q_value(self, state, action):
        return self.q_table[state][action]

    def greedy_action_selection(self, state):
        """
        Selects action with the highest Q-value for the given state.
        """
        # Get all the Q-values for all possible actions for the state
        q_values = [self.get_Q_value(state, action) for action in self.acts]
        maxQ = max(q_values)
        # There might be cases where there are multiple actions with the same high q_value. Choose randomly then
        count_maxQ = q_values.count(maxQ)
        if count_maxQ > 1:
            # Get all the actions with the maxQ
            best_action_indexes = [i for i in range(len(self.acts)) if q_values[i] == maxQ]
            action_index = random.choice(best_action_indexes)
        else:
            action_index = q_values.index(maxQ)
            
        return self.actions[action_index]

    def action_probs(self, state):
        """
        Returns the probability of taking each action in the next state.
        """
        next_state_probs = [self.epsilon/len(self.acts)] * len(self.acts)
        best_action = self.greedy_action_selection(state)
        next_state_probs[best_action] += (1.0 - self.epsilon)

        return next_state_probs

    def take_action(self, state):# epsilon-greedy
        # Choose a random action
        if random.random() < self.epsilon:
            action = random.choice(self.acts)
        # Choose the greedy action
        else:
            action = self.greedy_action_selection(state)
        
        return action

    def learn(self, state_old, state_new, action_old, reward):
        """
        Expected Sarsa update
        """
        next_state_probs = self.action_probs(next_state, self.epsilon) # Probability for taking each action in next state
        q_next_state = [self.get_Q_value(next_state, action) for action in self.acts] # Q-values for each action in next state
        next_state_expectation = sum([a*b for a, b in zip(next_state_probs, q_next_state)])

        q_current = self.Q.get((state, action), None) # If this is the first time the state action pair is encountered
        if q_current is None:
            self.Q[(state, action)] = reward
        else:
            self.Q[(state, action)] = q_current + (self.alpha * (reward + self.gamma * next_state_expectation - q_current))