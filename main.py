import time

from env import IntEnv
from agent import Agent
from logger import CustomLogger

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
action_space = {
    'HAP_LOOK':HAP_LOOK, 
    'SAD_LOOK':SAD_LOOK, 
    'FEA_LOOK':FEA_LOOK, 
    'ANG_LOOK':ANG_LOOK}

alpha = 0.4
gamma = 0.9
epsilon = 0.15

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


if __name__=='__main__':
    ## Init Environment and Agent
    # TODO: 
    # 1. proper input param lists
    # 2. proper initialization
    agent = Agent(
        s_ext = ext_state_space, 
        s_int = int_state_space, 
        acts = action_space,
        alpha = alpha,
        gamma = gamma)
    
    int_env = IntEnv(homeo_vars)## 1. input params
    
    log = CustomLogger('test.log')
    
    cnt = 0
    t0 = time.perf_counter()

    ext_states_old = get_ext_states(INPUT_PROMPT)
    int_state_old, well_being = int_env.update(ext_states_old, cnt)
    
    action_old = agent.take_action(ext_states_old, int_state_old)
    wb_prev = well_being

    log.step_log(cnt=cnt, s_ext=ext_states_old, s_int=int_state_old, wb=well_being, reward=None, action=action_old, t_st = t0)

    while True:
        cnt += 1
        t_start = time.perf_counter()

        ext_states_new = get_ext_states(INPUT_PROMPT)
        int_state_new, well_being = int_env.update(ext_states_new, cnt)##
        
        if well_being == WB_MAX:
            ## TODO: concurrent control: multi_threading
            ## reward = None, action = SUCCESS
            send_action_cmd(SUCCESS)
            
            log.step_log(cnt=cnt, s_ext=ext_states_new, s_int=int_state_new, wb=well_being, reward=None, action='SUCCESS', t_st=t_start)
            break
        else:
            if well_being == WB_MIN:
                ## TODO: concurrent control: multi_threading
                ## reward = None, action = FAIL
                send_action_cmd(FAIL)
                
                log.step_log(cnt=cnt, s_ext=ext_states_new, s_int=int_state_new, wb=well_being, reward=None, action='FAIL', t_st=t_start)
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
                ## TODO: concurrent control: multi_threading
                action_new = agent.take_action(ext_states_new, int_state_new)
                send_action_cmd(action_new)
                
                agent.learn(ext_states_old, int_state_old, ext_states_new, int_state_new, action_old, reward, epsilon)
                
                log.step_log(cnt=cnt, s_ext=ext_states_new, s_int=int_state_new, wb=well_being, reward=reward, action=action_new, t_st=t_start)

                ext_states_old = ext_states_new
                int_state_old = int_state_new
                action_old = action_new

    log.term_log(t0)

# END_OF_FILE