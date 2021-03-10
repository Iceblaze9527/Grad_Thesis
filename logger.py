import time
import logging

from param import ext_state_space, int_state_space, action_space, log_name

class Logger():
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            filename=log_name,
            filemode='w',
            format='%(message)s')
        logging.info('Start of interaction.')
    
    def step_log(self, cnt, s_ext, s_int, wb, reward, action, t_st):## TODO: automatic formatting
        action = action if isinstance(action, str) else action_space[action]
        logging.info('Step %5d: S_ext = %-19s, S_int = %-7s, Wb = %6.2f, Reward = %s, Action = %-8s, Elapsed_Time = %6.3f'
        %(cnt, ext_state_space[s_ext], int_state_space[s_int], wb, str(reward).ljust(7,' '), action, time.process_time() - t_st))
    
    def term_log(self, t0):
        logging.info('End of interaction.\nTotal Time: %8.3f'%(time.process_time() - t0))