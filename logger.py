import time
import logging

class CustomLogger():
    def __init__(self, logfile='test.log'):## TODO: time-related file names
        logging.basicConfig(
            level=logging.INFO,
            filename=logfile,
            filemode='w',
            format='%(message)s')
        logging.info('Start of interaction.')
    
    def step_log(self, cnt, s_ext, s_int, wb, reward, action, t_st):
        logging.info('Step %5d: S_ext = %-20s, S_int = %-7s, Wb = %6.2f, Reward = %s, Action = %-8s, Elapsed_Time = %6.3f'%(cnt, s_ext, s_int, wb, str(reward).ljust(7,' '), action, time.perf_counter() - t_st))
    
    def term_log(self, t0):
        logging.info('End of interaction.\n Total Time: %8.3f'%(time.perf_counter() - t0))