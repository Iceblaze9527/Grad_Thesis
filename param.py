from itertools import product

## 1. Agent Params
def get_ext_state_space(ext_state_vars):
    add_prefix = list(map(lambda var: [''.join(('DSB_',var)), ''.join(('ENV_',var))], ext_state_vars))
    state_product = list(product(add_prefix[1], add_prefix[0]))##TODO: for more external states
    ext_state_space = list(map(lambda item: ' & '.join((item[0], item[1])), state_product))
    return ext_state_space

ext_state_vars = ['FOOD', 'TAIL']
ext_state_space = get_ext_state_space(ext_state_vars)# index == flag
int_state_space = ['HAPPY', 'SAD', 'FEARFUL', 'ANGRY']# index == flag
action_space = ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK']# index == flag

alpha = 0.5 # in [0,1], low if previous knowledge is valued more, else new knowledge
gamma = 0.9 # in (0,1), can neither be too low (not convergent) nor too high (for small state space)
epsilon = 0.1 # can decline over time. Soft action selection policies include epsilon-greedy, epsilon-soft and softmax, etc..

## 2.

## 3. Logger Params
## TODO: time-related file names
log_name = 'test.log'