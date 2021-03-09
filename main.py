import time

from itertools import product

from env import IntEnv
from agent import Agent
from logger import CustomLogger

## helper funcs
def get_ext_state_space(ext_state_vars):
    add_prefix = list(map(lambda var: [''.join(('DSB_',var)), ''.join(('ENV_',var))], ext_state_vars))
    state_product = list(product(add_prefix[1], add_prefix[0]))## for more external states
    ext_state_spaces = list(map(lambda item: ' & '.join((item[0], item[1])), state_product))## for more external states
    return ext_state_spaces

## Main Params
INPUT_PROMPT = "Input external states, 1 for 'ENABLED', 0 for 'DISABLED'."

## Agent Params
ext_state_vars = ['FOOD', 'TAIL']
ext_state_space = get_ext_state_space(ext_state_vars)# index == flag
int_state_space = ['HAPPY', 'SAD', 'FEARFUL', 'ANGRY']# index == flag
action_space = ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK']# index == flag
SUCCESS = 5
FAIL = 7

alpha = 0.5 # in [0,1], low if former knowledge is valued more, else new knowledge
gamma = 0.9 # in (0,1), can neither be too low (not convergent) nor too high (for small state space)
epsilon = 0.1 # can decline over time. Soft action selection policies include epsilon-greedy, epsilon-soft and softmax

## IntEnv Params
## HomeoSys Params
homeo_vars = ['ENERGY', 'COMFORT']#optimal values
## ext_stimuli params
## increasing func params
## satisfaction time params
## satuation level params
## activation level params

## EmoSys Params
emo_motiv_mat = []##

## WbSys Params
WB_MAX = 100
WB_MIN = 0
## weight params

## control system
def get_ext_states(prompt):
    ext_states_str = input(prompt)
    
    ext_states_lst = list(ext_states_str)
    if not all([state in set(['0','1']) for state in ext_states_lst]):
        raise SyntaxError("Incorrect input format. Only 0s and 1s are allowed. Your input is '%s'. "%(ext_states_str))
    if not len(ext_states_lst) == len(ext_state_space):
        raise ValueError('Mismatched number of external states. External state num %d, input state num %d.'%(len(ext_state_space), len(ext_states_lst)))
    
    ext_states_lst = list(map(int, ext_states_lst))
    ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])## compute flag index
    
    return ext_states

def send_action_cmd(action):
    assert (action in [SUCCESS, FAIL])|(action in action_space), "Illegal action flag."

if __name__=='__main__':
    state = lambda int_state, ext_states: int_state << len(ext_state_vars) + ext_states
    ## Init Environment and Agent
    # TODO: 
    # 1. proper input param lists
    # 2. proper initialization
    agent = Agent(
        state_space = len(ext_state_space) * len(int_state_space),
        action_space = len(action_space),
        alpha = alpha,
        gamma = gamma,
        epsilon = epsilon)
    
    int_env = IntEnv(
        homeo_vars = homeo_vars)
    
    log = CustomLogger('test.log')## start signal
    
    ## Start Training
    cnt = 0
    t0 = time.perf_counter()

    ext_states_old = get_ext_states(INPUT_PROMPT)# return flag
    int_state_old, well_being = int_env.update(ext_states_old, cnt)# return flag (index)
    action_old = agent.take_action(state(int_state_old, ext_states_old))# return flag (index)
    wb_prev = well_being

    log.step_log(
        cnt=cnt, 
        s_ext=ext_state_space[ext_states_old],
        s_int=int_state_space[int_state_old], 
        wb=well_being, 
        reward=None, 
        action=action_old, 
        t_st = t0)

    while True:
        cnt += 1
        t_start = time.perf_counter()

        ext_states_new = get_ext_states(INPUT_PROMPT)# return flag
        int_state_new, well_being = int_env.update(ext_states_new, cnt)# return flag (index)
        
        if well_being == WB_MAX:## Halt
            send_action_cmd(SUCCESS)
            
            log.step_log(
                cnt=cnt, 
                s_ext=ext_state_space[ext_states_new],
                s_int=int_state_space[int_state_new], 
                wb=well_being, 
                reward=None, 
                action='SUCCESS', 
                t_st=t_start)
            
            break
        else:
            if well_being == WB_MIN:## Halt
                send_action_cmd(FAIL)
                
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_state_space[ext_states_new],
                    s_int=int_state_space[int_state_new], 
                    wb=well_being, 
                    reward=None, 
                    action='FAIL', 
                    t_st=t_start)
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
                action_new = agent.take_action(state(int_state_new, ext_states_new))# return flag (index)
                send_action_cmd(action_new)
                
                agent.learn(
                    state(int_state_old, ext_states_old), 
                    state(int_state_new, ext_states_new), 
                    action_old, 
                    reward)
                
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_state_space[ext_states_new],
                    s_int=int_state_space[int_state_new], 
                    wb=well_being, 
                    reward=reward, 
                    action=action_new, 
                    t_st=t_start)

                ext_states_old = ext_states_new
                int_state_old = int_state_new
                action_old = action_new
    ## Terminate Training
    log.term_log(t0)

# END_OF_FILE