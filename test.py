import logging
import time

NON_REW = 999

SUCCESS = 0
FAIL = 1

HAP_LOOK = 3
SAD_LOOK = 4
FEA_LOOK = 5
ANG_LOOK = 6

ext_state_space = ['FOOD', 'TAIL']
int_state_space = ['HAPPY', 'SAD', 'FEARFUL', 'ANGRY']
action_space = {
    'HAP_LOOK':HAP_LOOK, 
    'SAD_LOOK':SAD_LOOK, 
    'FEA_LOOK':FEA_LOOK, 
    'ANG_LOOK':ANG_LOOK}

if __name__ == '__main__':  
    ## write_init_log

    ext_states, int_state, well_being, reward, action = 'FOOD & NO_TAIL', 'HAPPY', 50, NON_REW, 'HAP_LOOK'
    wb_prev = well_being
    
    ## write_step_log

    while True:
        t_start = time.perf_counter()
        
        ext_states, int_state, well_being = 'FOOD & TAIL', 'SAD', well_being - 10
        
        if well_being == 100:
            reward = NON_REW
            action = 'SUCCESS'
            ## write_step_log
            break
        else:
            if well_being == 0:
                reward = NON_REW
                action = 'FAIL'
                ## write_step_log
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
                action = 'HAP_LOOK'
                time.sleep(1)
                ## write_step_log

    ## write_term_log

# import os

# print('Process (%s) start...' % os.getpid())
# pid = os.fork()

# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))