import sys 
sys.path.append("..") 

import numpy as np

from param import AGENT_PAR

np.random.seed(AGENT_PAR['rand_seed'])

class Agent():# Expected SARSA (On-policy implementation)
    _state_space = len(AGENT_PAR['ext_state_space'])
    _action_space = len(AGENT_PAR['action_space'])
    
    def __init__(self):
        self._q_table = np.random.normal(scale=AGENT_PAR['rand_scale'], size=(Agent._state_space, Agent._action_space))
        self.file = open(AGENT_PAR['logfile'], 'a')

        self._save_q_tab = lambda cnt: np.savetxt(fname=self.file, X=self._q_table, 
            fmt='%.3f', delimiter=',', newline='\n', header='Step %5d'%(cnt))
        
        self._save_q_tab(0)

    def _greedy_action_selection(self, state):
        q_max = (np.argmax(self._q_table[state, :])).reshape(-1)
        action = np.random.choice(q_max)
        return action

    def _action_probs(self, state):# epsilon-greedy
        best_action = self._greedy_action_selection(state)
        probas = AGENT_PAR['epsilon'] / Agent._action_space * np.ones(Agent._action_space)
        probas[best_action] += (1.0 - AGENT_PAR['epsilon'])
        return probas

    def take_action(self, ext_state):# epsilon-greedy
        if np.random.rand() < AGENT_PAR['epsilon']:
            return np.random.choice(Agent._action_space)
        else:
            return self._greedy_action_selection(ext_state)

    def learn(self, ext_states_old, ext_states_new, action_old, reward, cnt):
        state_new_probs = self._action_probs(ext_states_new).reshape(-1)
        state_new_q_val = (self._q_table[ext_states_new, :]).reshape(-1)
        state_new_expct = np.sum(state_new_probs * state_new_q_val)

        delta = AGENT_PAR['alpha'] * (reward + AGENT_PAR['gamma'] * state_new_expct - self._q_table[ext_states_old, action_old])
        self._q_table[ext_states_old, action_old] += delta
        
        self._save_q_tab(cnt)