import numpy as np

from param import ext_state_vars, ext_state_space, int_state_space, action_space, alpha, gamma, epsilon, q_tab_log_name

## TODO:
## 1. param bounds and time variants
## 2. Different Algos: Inheritance and Polymorphism

class Agent():# Expected SARSA (On-policy implementation)
    _state_space = len(ext_state_space) * len(int_state_space)
    _action_space = len(action_space)
    
    def __init__(self):
        self._q_table = np.random.rand(_state_space, _action_space)
        self._file = open(q_tab_log_name, 'a')
        self._save_q_tab(self._file, self._q_table, 0)
    
    @staticmethod
    def _save_q_tab(file, q_tab, cnt):
        np.savetxt(fname=file, X=q_tab, fmt='%.3f', delimiter=',', newline='\n', header='Step %5d'%(cnt))
    
    @staticmethod
    def _get_state(int_state, ext_states):
        return (int_state << len(ext_state_vars)) + ext_states

    def _greedy_action_selection(self, state):
        q_max = (np.argmax(self._q_table[state, :])).reshape(-1)
        action = np.random.choice(q_max)
        return action

    def _action_probs(self, state):# epsilon-greedy
        best_action = self._greedy_action_selection(state)
        probas = epsilon / _action_space * np.ones(_action_space)
        probas[best_action] += (1.0 - epsilon)
        return probas

    def take_action(self, int_state, ext_states):# epsilon-greedy
        if np.random.rand() < epsilon:
            return np.random.choice(_action_space)
        else:
            return self._greedy_action_selection(self._get_state(int_state, ext_states))

    def learn(self, int_state_old, ext_states_old, int_state_new, ext_states_new, action_old, reward, cnt):
        state_old = self._get_state(int_state_old, ext_states_old)
        state_new = self._get_state(int_state_new, ext_states_new)

        state_new_probs = self._action_probs(state_new).reshape(-1)
        state_new_q_val = (self._q_table[state_new, :]).reshape(-1)
        state_new_expct = np.sum(state_new_probs * state_new_q_val)

        delta = alpha * (reward + gamma * state_new_expct - self._q_table[state_old, action_old])
        self._q_table[state_old, action_old] += delta
        
        self._save_q_tab(self._file, self._q_table, cnt)