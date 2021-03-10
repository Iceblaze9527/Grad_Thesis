from param import ext_state_vars, ext_state_space, action_space

## TODO: 
# 1. sensor input & actuator output

def get_ext_states():
    ext_states_str = input("Input external states, 1 for 'ENABLED', 0 for 'DISABLED'.")
    
    ext_states_lst = list(ext_states_str)
    if not all([state in set(['0','1']) for state in ext_states_lst]):
        print("Incorrect input format. Only 0s and 1s are allowed. Your input is '%s'. "%(ext_states_str))
        return -1
    if not len(ext_states_lst) == len(ext_state_vars):
        print('Mismatched number of external states. External state num %d, input state num %d.'%(len(ext_state_space), len(ext_states_lst)))
        return -1
    
    ext_states_lst = list(map(int, ext_states_lst))
    ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])
    
    return ext_states

def send_action_cmd(action):
    assert (action in ['SUCCESS', 'FAIL'])|(action in range(len(action_space))), "Illegal action flag."