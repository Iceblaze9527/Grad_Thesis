import time
import logging

from param import AGENT_PAR, MAIN_LOG

class Logger():
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            filename=MAIN_LOG,
            filemode='w',
            format='%(message)s')
        logging.info('Start of interaction.')
    
    def step_log(self, cnt, s_ext, s_int, wb, reward, action, t_st):
        action = action if isinstance(action, str) else AGENT_PAR['action_space'][action]
        logging.info('Step %5d: S_ext = %-19s, S_int = %-5s, Wb = %6.2f, Reward = %s, Action = %-8s, Elapsed_Time = %6.3f'
        %(cnt, AGENT_PAR['ext_state_space'][s_ext], AGENT_PAR['int_state_space'][s_int], wb, str(reward).ljust(7,' '), action, time.process_time() - t_st))
    
    def term_log(self, t0):
        logging.info('End of interaction.\nTotal Time: %8.3f'%(time.process_time() - t0))