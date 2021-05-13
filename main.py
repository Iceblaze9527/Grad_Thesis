import time

from agent import Agent
from env import IntEnv
from logger import Logger
from inputdev import InputDevices
from outputdev import OutputDevices

if __name__=='__main__':
    agent = Agent()
    int_env = IntEnv()
    log = Logger()
    inputs = InputDevices()
    outputs = OutputDevices()
    
    cnt = 0
    t0 = time.process_time()

    ext_states_old = inputs.get_ext_states()
    
    well_being = int_env.step(ext_states_old, cnt)
    action_old = agent.take_action(ext_states_old)
    wb_prev = well_being

    log.step_log(
        cnt=cnt, 
        s_ext=ext_states_old,
        wb=well_being, reward=None, 
        action=action_old, 
        t_st=t0)

    while True:
        cnt += 1
        t_start = time.process_time()

        ext_states_new = inputs.get_ext_states()
        
        well_being = int_env.step(ext_states_new, cnt)
        
        if well_being == int_env.wb_max:
            outputs.exec_action(4)##
            log.step_log(
                cnt=cnt, 
                s_ext=ext_states_new,
                wb=well_being, reward=None, 
                action='SUCCESS', 
                t_st=t_start)
            break
        else:
            if well_being == int_env.wb_min:
                outputs.exec_action(5)##
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_states_new,
                    wb=well_being, reward=None, 
                    action='FAIL', 
                    t_st=t_start)
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
                action_new = agent.take_action(ext_states_new)
                outputs.exec_action(action_new)
                
                agent.learn(ext_states_old, ext_states_new, action_old, reward, cnt)
                
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_states_new,
                    wb=well_being, reward=reward, 
                    action=action_new, 
                    t_st=t_start)

                ext_states_old = ext_states_new
                action_old = action_new

    log.term_log(t0)
    
    (agent.file).close()
    (int_env.file).close()
    inputs.closeall()
    outputs.closeall()
    
    exit()

# END_OF_FILE