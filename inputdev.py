import time

import numpy as np

import smbus
from gpiozero import Button
import RPi.GPIO as GPIO

## TODO: param.py
ext_state_vars = ['FOOD', 'TOXIN', 'BOOP', 'PULL']

#FOOD: BUTTON
BUTTON_1 = 27
#TOXIN: BUTTON
BUTTON_2 = 25
#BOOP: TOUCH SENSOR
TOUCH = 23
#PULL: JOYSTICK
ADDR = 0x48
AIN0 = 0x00
AIN1 = 0x01
THRESHOLD = 192

TIME_LIMIT = 2#secs
SAMPLE_INTERVAL = 0.04#sec
MIN_EFF_INPUT_LEN = 5#samples

class InputDevices():
    def __init__(self):
        self.button_1 = Button(pin=BUTTON_1, pull_up=True)
        self.button_2 = Button(pin=BUTTON_2, pull_up=True)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TOUCH, GPIO.IN)

        self.bus = smbus.SMBus(1)
        self.bus.write_byte(ADDR,AIN0)
        self.bus.read_byte(ADDR)#
    
    def get_ext_states(self):
        t0 = time.time()
        ext_state_samples = np.zeros((1, len(ext_state_vars)), dtype=np.uint8)
        
        while (time.time() - t0 < TIME_LIMIT):
            sample = np.array([(self.button_1).value, (self.button_2).value, GPIO.input(TOUCH), \
                1 if (self.bus).read_byte(ADDR) > THRESHOLD else 0]).reshape(1,-1)
            ext_state_samples = np.concatenate((ext_state_samples, sample), axis=0)

            time.sleep(SAMPLE_INTERVAL)

        ext_states_lst = []
        for col in range(len(ext_state_vars)):
            samples = ext_state_samples[1:,col]
            differ = np.diff(samples)
            pulse = np.flatnonzero(differ)
            
            if len(pulse) == 0:
                ext_states_lst.append(1 if samples[-1] == 1 else 0)
                continue
            
            voltage = np.split(samples, (pulse + 1))
            high_cnt = map(lambda x:len(x), voltage[1::2] if differ[pulse[0]] == 1 else voltage[::2])
            ext_states_lst.append(1 if max(high_cnt) >= MIN_EFF_INPUT_LEN else 0)
        
        ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])

        return ext_states

    def closeall(self):
        (self.button_1).close()
        (self.button_2).close()
        GPIO.cleanup(TOUCH)
        (self.bus).close()

# if __name__ == '__main__':
#     try:
#         inputs = InputDevices()
#         while True:
#             print(inputs.get_ext_states())
#             time.sleep(0.05)
#     except KeyboardInterrupt:
#         inputs.closeall()
#         exit()