from inputdev import InputDevices
from outputdev import OutputDevices

try:
    inputs = InputDevices()
    outputs = OutputDevices()
    
    ext_states_old = inputs.get_ext_states()
    
    while True:
        ext_states_new = inputs.get_ext_states()
        print(ext_states_new)
        outputs.exec_action(5)

except KeyboardInterrupt:
    inputs.closeall()
    outputs.closeall()
    exit()