import time

from logger import CustomLogger

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
    log = CustomLogger('test.log')

    cnt = 0
    t0 = time.perf_counter()
    
    log.init_log()

    ext_states, int_state, well_being, reward, action = 'FOOD & NO_TAIL', 'HAPPY', 50, None, 'HAP_LOOK'
    wb_prev = well_being
    
    log.step_log(cnt=cnt, s_ext=ext_states, s_int=int_state, wb=well_being, reward=reward, action=action, t_st = t0)

    while True:
        cnt += 1
        t_start = time.perf_counter()
        
        ext_states, int_state, well_being = 'FOOD & TAIL', 'SAD', well_being - 10
        
        if well_being == 100:
            reward = None
            action = 'SUCCESS'
            log.step_log(cnt=cnt, s_ext=ext_states, s_int=int_state, wb=well_being, reward=reward, action=action, t_st=t_start)
            break
        else:
            if well_being == 0:
                reward = None
                action = 'FAIL'
                log.step_log(cnt=cnt, s_ext=ext_states, s_int=int_state, wb=well_being, reward=reward, action=action, t_st=t_start)
                break
            else:
                reward = well_being - wb_prev
                action = 'HAP_LOOK'
                time.sleep(1)
                log.step_log(cnt=cnt, s_ext=ext_states, s_int=int_state, wb=well_being, reward=reward, action=action, t_st=t_start)
                wb_prev = well_being

    log.term_log(t0)

# import os

# print('Process (%s) start...' % os.getpid())
# pid = os.fork()

# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))