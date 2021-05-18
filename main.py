import time

from algo.agent import Agent
from algo.env import IntEnv

from ctrl.inputdev import InputDevices
from ctrl.outputdev import OutputDevices

from logger import Logger

if __name__=='__main__':
    agent = Agent()
    int_env = IntEnv()
    inputs = InputDevices()
    outputs = OutputDevices()
    log = Logger()
    
    cnt = 1
    t0 = time.process_time()

    ext_states_old = inputs.get_ext_states()
    reward = int_env.step(ext_states_old, cnt)
    action_old = agent.take_action(ext_states_old)

    log.step_log(
        cnt=cnt, 
        s_ext=ext_states_old,
        wb=int_env.wb, reward=reward, 
        action=action_old, 
        t_st=t0)

    while True:
        cnt += 1
        t_start = time.process_time()

        ext_states_new = inputs.get_ext_states()
        reward = int_env.step(ext_states_new, cnt)
        
        if int_env.wb == int_env.wb_max:
            outputs.exec_action(4)##
            log.step_log(
                cnt=cnt, 
                s_ext=ext_states_new,
                wb=int_env.wb, reward=reward, 
                action='SUCCESS', 
                t_st=t_start)
            break
        else:
            if int_env.wb == int_env.wb_min:
                outputs.exec_action(5)##
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_states_new,
                    wb=int_env.wb, reward=reward, 
                    action='FAIL', 
                    t_st=t_start)
                break
            else:
                action_new = agent.take_action(ext_states_new)
                outputs.exec_action(action_new)
                
                agent.learn(ext_states_old, ext_states_new, action_old, reward, cnt)
                
                log.step_log(
                    cnt=cnt, 
                    s_ext=ext_states_new,
                    wb=int_env.wb, reward=reward, 
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