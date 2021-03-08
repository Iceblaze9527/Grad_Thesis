INPUT_PROMPT = "Input external states, 1 for 'ENABLED', 0 for 'DISABLED'. "

SUCCESS = 0
FAIL = -1

HAP_LOOK = 3
SAD_LOOK = 4
FEA_LOOK = 5
ANG_LOOK = 6

ext_state_space = ['FOOD', 'TAIL']## Kronecker Product
action_space = [HAP_LOOK, SAD_LOOK, FEA_LOOK, ANG_LOOK]

## test passed:
def get_ext_states(prompt):
    pass

def send_action_cmd(action):
    pass

if __name__ == '__main__':
    pass


# import os

# print('Process (%s) start...' % os.getpid())
# pid = os.fork()

# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))