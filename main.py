import time
import logging

from env import IntEnv
from agent import Agent

# TODO:
# 1. encode state and action space
# 2. specify internal env params

## Main Params
INPUT_PROMPT = "Input external states, 1 for 'ENABLED', 0 for 'DISABLED'."

SUCCESS = 0
FAIL = 1

HAP_LOOK = 3
SAD_LOOK = 4
FEA_LOOK = 5
ANG_LOOK = 6

## Agent Params
ext_state_space = ['FOOD', 'TAIL']## Kronecker Product
int_state_space = ['HAPPY', 'SAD', 'FEARFUL', 'ANGRY']## Kronecker Product
action_space = [HAP_LOOK, SAD_LOOK, FEA_LOOK, ANG_LOOK]

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
    ## TODO: concurrent control: multi_threading
    ext_states_str = input(prompt)
    
    ext_states_lst = list(ext_states_str)
    if not all([state in set(['0','1']) for state in ext_states_lst]):
        raise SyntaxError("Incorrect input format. Only 0s and 1s are allowed. Your input is '%s'. "%(ext_states_str))
    if not len(ext_states_lst) == len(ext_state_space):
        raise ValueError('Mismatched number of external states. External state num %d, input state num %d.'%(len(ext_state_space), len(ext_states_lst)))
    
    ext_states = map(int, ext_states_lst)
    return ext_states

def send_action_cmd(action):
    assert (action in [SUCCESS, FAIL])|(action in action_space), "Illegal action flag."
    pass


if __name__=='__main__':
    cnt = 0

    ## Init Environment and Agent
    # TODO: 
    # 1. proper input param lists
    # 2. proper initialization
    agent = Agent(
        s_ext = ext_state_space, 
        s_int = int_state_space, 
        a = action_space)## 1. input params
    int_env = IntEnv(homeo_vars)## 1. input params
    
    ext_states = get_ext_states(INPUT_PROMPT)
    int_state, well_being = int_env.update(ext_states, cnt)
    
    action = agent.act(ext_states, int_state)
    wb_prev = well_being
    
    # print(ext_states, int_state, well_being, reward=None, action)#
    t0 = time.perf_counter()
    while True:
        cnt += 1
        t_start = time.perf_counter()

        ext_states = get_ext_states(INPUT_PROMPT)
        int_state, well_being = int_env.update(ext_states, cnt)##
        
        if well_being == WB_MAX:
            ## TODO: concurrent control: multi_threading
            send_action_cmd(SUCCESS)
            # print('Success!')#
            
            # print(cnt)#
            # print(time.perf_counter() - t_start)#
            # print(ext_states, int_state, well_being, reward=None, action=SUCCESS)#
            break
        else:
            if well_being == WB_MIN:
                ## TODO: concurrent control: multi_threading
                send_action_cmd(FAIL)
                # print('Fail!')#
                
                # print(cnt)#
                # print(time.perf_counter() - t_start)#
                # print(ext_states, int_state, well_being, reward=None, action=FAIL)#
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
        
        action = agent.act(ext_states, int_state)
        
        ## TODO: concurrent control: multi_threading
        send_action_cmd(action)
        agent.learn(ext_states, int_state, reward)
        
        # print(cnt)#
        # print(time.perf_counter() - t_start)#
        # print(ext_states, int_state, well_being, reward, action)# 

    # print('End of interaction.')#
    # print(time.perf_counter() - t0)#

# END_OF_FILE