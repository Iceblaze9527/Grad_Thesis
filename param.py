import os
import time
from itertools import product

import numpy as np

def __get_ext_state_space(ext_state_vars):
    add_prefix = list(map(lambda var: [''.join(('DSB_',var)), ''.join(('ENV_',var))], ext_state_vars))[::-1]
    state_product = list(product(*add_prefix))
    ext_state_space = list(map(lambda item: ' & '.join(item), state_product))
    return ext_state_space

def __get_filename(filename, parent_path):
    timestamp = time.strftime("%y%m%d_%H.%M.%S", time.localtime()) 
    dir_path = os.path.join(parent_path, timestamp)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return os.path.join(dir_path, filename)

## TODO: Param time variants
AGENT_PAR = {'ext_state_vars': ['FOOD', 'TOXIN', 'BOOP', 'PULL'], 
    'ext_state_space': [], 
    'action_space': ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK'],
    'alpha': 0.5,# low if previous knowledge is valued more, else new knowledge
    'gamma': 0.9,# can neither be too low (not convergent) nor too high (for small state space)
    'epsilon': 0.1# can decline over time. Soft action selection policies include epsilon-greedy, epsilon-soft and softmax, etc..
    }

AGENT_PAR['ext_state_space'] = __get_ext_state_space(AGENT_PAR['ext_state_vars'])

assert (AGENT_PAR['alpha'] >= 0) & (AGENT_PAR['alpha'] <= 1)
assert (AGENT_PAR['gamma'] > 0) & (AGENT_PAR['gamma'] < 1)
assert (AGENT_PAR['epsilon'] > 0) & (AGENT_PAR['epsilon'] < 1)

INTENV_PAR = {
    'homeo_vars': ['ENERGY', 'COMFORT'],
    'hv_maxs': np.array([100,100]),
    'hv_mins': np.array([0,0]),
    'coef_hv_ext_st': np.array([[10,-8,0,0],[0,0,10,-8]]),
    'step_decays': [], ## a function list, return (hv_func[cnt] - hv_func[cnt - 1]) based on hv_func[cnt - 1]
    'act_levels': np.array([5,5]),
    'motiv_weights': np.array([0.5,0.5]),
    'wb_limit':[0,100] ## wb_min, wb_max
}

linear_decay = lambda hv_old: 3
## TODO: more complex decay functions
INTENV_PAR['step_decays'] = [linear_decay, linear_decay]

assert len(INTENV_PAR['hv_maxs']) == len(INTENV_PAR['homeo_vars'])
assert len(INTENV_PAR['hv_mins']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['hv_mins'] < INTENV_PAR['hv_maxs']).all()
assert (INTENV_PAR['hv_mins'] >= 0).all()

assert INTENV_PAR['coef_hv_ext_st'].shape == (len(INTENV_PAR['homeo_vars']), len(AGENT_PAR['ext_state_vars'])) 
## max(c_hs[hv, :]) > max(decay(hv)) (there is always a means to increase it)

assert len(INTENV_PAR['act_levels']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['act_levels'] > 0).all()

assert len(INTENV_PAR['step_decays']) == len(INTENV_PAR['homeo_vars'])
assert len(INTENV_PAR['motiv_weights']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['motiv_weights'] > 0).all()

assert INTENV_PAR['wb_limit'][0]< INTENV_PAR['wb_limit'][1]

## estimate reward: reward ~ sum(i)(theta[i] * (hv[i][t+1] - hv[i][t]))
## estimate wb: wb = wb_max - sum(i)(theta[i] * motiv[i]) ~ wb_max - sum(i)(theta[i] * (hv_max[i] - hv_min[i]))
## estimate q-val: delta = alpha * (reward + gamma * ~avr(q(s[t+1], a[:])) - q(s[t], a[t]))

LOG_PATH = './logs'
MAIN_LOG = __get_filename('train.log', LOG_PATH)
AGENT_LOG = __get_filename('agent.txt', LOG_PATH)
INTENV_LOG = __get_filename('int_env.txt', LOG_PATH)

RAND_SEED = 17