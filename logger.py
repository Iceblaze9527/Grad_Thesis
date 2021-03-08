import time
import logging

class CustomLogger():
    def __init__(self, logfile='test.log'):## TODO: time-related file names
        logging.basicConfig(
            level=logging.INFO,
            filename=logfile,
            filemode='w',
            format='%(message)s')
        self.cnt = 0
        self.t0 = time.perf_counter()
    
    def write_init_log(self):
        logging.info('Start of interaction.')
    
    def write_step_log(self, ext_states, int_state, well_being, reward, action, t_start):## TODO: property & decorator
        logging.info('Step %5d: S_ext = %-20s, S_int = %-7s, Wb = %6.2f, Reward = %6.2f, Action = %-8s, Elapsed_Time = %6.3f'
            %(self.cnt, ext_states, int_state, well_being, reward, action, time.perf_counter() - t_start))
        self.cnt += 1
    
    def write_term_log(self):
        logging.info('End of interaction. Total Time: %8.3f'%(time.perf_counter() - self.t0))