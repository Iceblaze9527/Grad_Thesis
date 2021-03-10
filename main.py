import time

import control as ctrl

from env import IntEnv
from agent import Agent
from logger import Logger

WB_MAX = 100
WB_MIN = 0


if __name__=='__main__':
    agent = Agent()
    int_env = IntEnv()
    log = Logger()
    
    t0 = time.process_time()

    ext_states_old = ctrl.get_ext_states()
    if ext_states_old == -1:
        exit(1)
    
    int_state_old, well_being = int_env.update(ext_states_old, agent.cnt)# return flag (index)
    action_old = agent.take_action(int_state_old, ext_states_old)
    wb_prev = well_being

    log.step_log(
        cnt=agent.cnt, 
        s_ext=ext_states_old, s_int=int_state_old,
        wb=well_being, reward=None, 
        action=action_old, 
        t_st=t0)

    while True:
        t_start = time.process_time()

        ext_states_new = ctrl.get_ext_states()
        if ext_states_new == -1:
            continue
        
        agent.cnt += 1
        int_state_new, well_being = int_env.update(ext_states_new, agent.cnt)# return flag (index)
        
        if well_being == WB_MAX:## Halt
            ctrl.send_action_cmd('SUCCESS')
            log.step_log(
                cnt=agent.cnt, 
                s_ext=ext_states_new, s_int=int_state_new,
                wb=well_being, reward=None, 
                action='SUCCESS', 
                t_st=t_start)
            break
        else:
            if well_being == WB_MIN:## Halt
                ctrl.send_action_cmd('FAIL')
                log.step_log(
                    cnt=agent.cnt, 
                    s_ext=ext_states_new, s_int=int_state_new,
                    wb=well_being, reward=None, 
                    action='FAIL', 
                    t_st=t_start)
                break
            else:
                reward = well_being - wb_prev
                wb_prev = well_being
                action_new = agent.take_action(int_state_new, ext_states_new)
                ctrl.send_action_cmd(action_new)##TODO: parallel
                
                agent.learn(
                    int_state_old, ext_states_old, 
                    int_state_new, ext_states_new, 
                    action_old, reward)
                
                log.step_log(
                    cnt=agent.cnt, 
                    s_ext=ext_states_new, s_int=int_state_new,
                    wb=well_being, reward=reward, 
                    action=action_new, 
                    t_st=t_start)

                ext_states_old = ext_states_new
                int_state_old = int_state_new
                action_old = action_new

    log.term_log(t0)

# END_OF_FILE