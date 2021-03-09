import random

class Agent:
    def __init__(self, s_ext, s_int, acts, alpha = 0.4, gamma=0.9):
        """
        The Q-values will be stored in a dictionary. Each key will be of the format: ((x, y), a). 
        params:
            actions (list): A list of all the possible action values.
            alpha (float): step size
            gamma (float): discount factor
        """

        #self.s_ext = s_ext
        #self.s_int = s_int
        self.acts = acts

        self.alpha = alpha
        self.gamma = gamma

        self.Q = {}##Q-table

    def get_Q_value(self, s_ext, s_int, action):##
        """
        Get q value for a state action pair.
        params:
            state (tuple): (x, y) coords in the grid
            action (int): an integer for the action
        """
        pass
        #return self.Q.get((state, action), 0.0) # Return 0.0 if state-action pair does not exist

    def take_action(self, s_ext, s_int, epsilon=0.1):# epsilon-greedy
        # Choose a random action
        if random.random() < epsilon:
            action = random.choice(self.acts)
        # Choose the greedy action
        else:
            action = self.greedy_action_selection(state)##s_ext x s_int
        
        return action

    def learn(self, s_ext_old, s_int_old, s_ext_new, s_int_new, action_old, reward, epsilon):
        """
        Expected Sarsa update
        """
        next_state_probs = self.action_probs(next_state, epsilon) # Probability for taking each action in next state
        q_next_state = [self.get_Q_value(next_state, action) for action in self.actions] # Q-values for each action in next state
        next_state_expectation = sum([a*b for a, b in zip(next_state_probs, q_next_state)])

        q_current = self.Q.get((state, action), None) # If this is the first time the state action pair is encountered
        if q_current is None:
            self.Q[(state, action)] = reward
        else:
            self.Q[(state, action)] = q_current + (self.alpha * (reward + self.gamma * next_state_expectation - q_current))

    def greedy_action_selection(self, state):
        """
        Selects action with the highest Q-value for the given state.
        """
        # Get all the Q-values for all possible actions for the state
        q_values = [self.get_Q_value(state, action) for action in self.actions]
        maxQ = max(q_values)
        # There might be cases where there are multiple actions with the same high q_value. Choose randomly then
        count_maxQ = q_values.count(maxQ)
        if count_maxQ > 1:
            # Get all the actions with the maxQ
            best_action_indexes = [i for i in range(len(self.actions)) if q_values[i] == maxQ]
            action_index = random.choice(best_action_indexes)
        else:
            action_index = q_values.index(maxQ)
            
        return self.actions[action_index]

    def action_probs(self, state, epsilon):
        """
        Returns the probability of taking each action in the next state.
        """
        next_state_probs = [epsilon/len(self.actions)] * len(self.actions)
        best_action = self.greedy_action_selection(state)
        next_state_probs[best_action] += (1.0 - epsilon)

        return next_state_probs