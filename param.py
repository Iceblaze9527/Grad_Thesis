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

#-----------
# Logs
#-----------

LOG_PATH = './logs'
MAIN_LOG = __get_filename('train.log', LOG_PATH)

#-----------
# Agents
#-----------

AGENT_PAR = {'ext_state_vars': ['FOOD', 'TOXIN', 'BOOP', 'PULL'], 
    'ext_state_space': [], 
    'action_space': ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK'],
    'alpha': 0.5,# low if previous knowledge is valued more, else new knowledge
    'gamma': 0.9,# can neither be too low (not convergent) nor too high (for small state space)
    'epsilon': 0.1,# can decline over time. Soft action selection policies include epsilon-greedy, epsilon-soft and softmax, etc..
    'rand_seed': 17,
    'rand_scale': 1,# the scale for init wb sampled from binom distrib for the q-table
    'logfile' = __get_filename('agent.txt', LOG_PATH)
    }

AGENT_PAR['ext_state_space'] = __get_ext_state_space(AGENT_PAR['ext_state_vars'])

assert (AGENT_PAR['alpha'] >= 0) & (AGENT_PAR['alpha'] <= 1)
assert (AGENT_PAR['gamma'] > 0) & (AGENT_PAR['gamma'] < 1)
assert (AGENT_PAR['epsilon'] > 0) & (AGENT_PAR['epsilon'] < 1)
assert (AGENT_PAR['rand_scale'] > 0)

#-----------
# Internal Environment
#-----------

INTENV_PAR = {
    'homeo_vars': ['ENERGY', 'COMFORT'],
    'hv_maxs': np.array([100,100]),
    'hv_mins': np.array([0,0]),
    'coef_hv_ext_st': np.array([[10,-8,0,0],[0,0,10,-8]]),
    'step_decays': [], # a function list, return (hv_func[cnt] - hv_func[cnt - 1]) based on hv_func[cnt - 1]
    'act_levels': np.array([5,5]),
    'motiv_weights': np.array([0.5,0.5]),
    'wb_limit':[0,100], # wb_min, wb_max
    'rand_seed': 17,
    'init_expct': 0.6, # the expct of init hv = hv_min + init_expct * (hv_max - hv_min)
    'logfile': = __get_filename('int_env.txt', LOG_PATH)
}

linear_decay = lambda hv_old: 3
INTENV_PAR['step_decays'] = [linear_decay, linear_decay]

assert len(INTENV_PAR['hv_maxs']) == len(INTENV_PAR['homeo_vars'])
assert len(INTENV_PAR['hv_mins']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['hv_mins'] < INTENV_PAR['hv_maxs']).all()
assert (INTENV_PAR['hv_mins'] >= 0).all()
assert INTENV_PAR['coef_hv_ext_st'].shape == (len(INTENV_PAR['homeo_vars']), len(AGENT_PAR['ext_state_vars'])) 
assert len(INTENV_PAR['step_decays']) == len(INTENV_PAR['homeo_vars'])
assert len(INTENV_PAR['act_levels']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['act_levels'] > 0).all()
assert len(INTENV_PAR['motiv_weights']) == len(INTENV_PAR['homeo_vars'])
assert (INTENV_PAR['motiv_weights'] > 0).all()
assert INTENV_PAR['wb_limit'][0]< INTENV_PAR['wb_limit'][1]
assert (INTENV_PAR['init_expct'] > 0) & (INTENV_PAR['init_expct'] < 1)

assert np.sum(INTENV_PAR['motiv_weights'] * (INTENV_PAR['hv_maxs'] - INTENV_PAR['act_levels'] - INTENV_PAR['hv_mins'])) >= np.diff(INTENV_PAR['wb_limit'])
##

#-----------
# Notes
#-----------

## max(c_hs[hv, :]) > max(decay(hv)) (there is always a means to increase/decrease it)

"""
1.1 examine the reward expectation under the supposition that each external state appears under the same probability (do a quick experiment to get an average! conditional values in the dynamics make calculation not worth the effort)
1.2 tune the params to keep the expectation as close to zero as possible. this means under the supposition above, the well-being increase/decrease is purely a result of effective/destructive learning, rather than a natural drift caused by the inputs.
 - positive drift may make training faster, but is theoretically more like a trick, i.e., external states are on the whole favorable to the agent
 - negative drift needs more effort to counter, and it also implies that external states are on the whole hostile to the agent
 - so both are not encouraged
2. estimate reward: reward ~ sum(i)(theta[i] * (hv[i][t+1] - hv[i][t]))
3. estimate q-val: delta = alpha * (reward + gamma * ~avr(q(s[t+1], a[:])) - q(s[t], a[t]))
4. estimate wb: wb = wb_max - sum(i)(theta[i] * motiv[i]) ~ wb_max - sum(i)(theta[i] * (hv_max[i] - hv_min[i]))
"""
