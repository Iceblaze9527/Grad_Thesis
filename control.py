from param import ext_state_space, action_space ##

## control system
def get_ext_states(prompt):
    ext_states_str = input(prompt)
    
    ext_states_lst = list(ext_states_str)
    if not all([state in set(['0','1']) for state in ext_states_lst]):
        raise SyntaxError("Incorrect input format. Only 0s and 1s are allowed. Your input is '%s'. "%(ext_states_str))
    if not len(ext_states_lst) == len(ext_state_space):
        raise ValueError('Mismatched number of external states. External state num %d, input state num %d.'%(len(ext_state_space), len(ext_states_lst)))
    
    ext_states_lst = list(map(int, ext_states_lst))
    ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])
    
    return ext_states

def send_action_cmd(action):
    assert (action in ['SUCCESS', 'FAIL'])|(action in action_space), "Illegal action flag."