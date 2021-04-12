import time

import numpy as np

from inputdev import InputDevices
from outputdev import OutputDevices

try:
    inputs = InputDevices()
    outputs = OutputDevices()
    
    ext_states_old = inputs.get_ext_states()
    
    while True:
        ext_states_new = inputs.get_ext_states()
        print(ext_states_new)
        action = np.random.randint(0,4)#
        outputs.exec_action(action)
    
        time.sleep(0.05)

except KeyboardInterrupt:
    inputs.closeall()
    outputs.closeall()
    exit()