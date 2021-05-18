import sys 
sys.path.append("..") 

import time

import smbus
import numpy as np
import RPi.GPIO as GPIO
from gpiozero import Button

from param import INPUT_PAR

class InputDevices():
    def __init__(self):
        self.button_1 = Button(pin=INPUT_PAR['button_food'], pull_up=True)
        self.button_2 = Button(pin=INPUT_PAR['button_toxin'], pull_up=True)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(INPUT_PAR['boop'], GPIO.IN)

        self.bus = smbus.SMBus(1)
        self.bus.write_byte(INPUT_PAR['adc_addr'],INPUT_PAR['adc_ain0'])
        self.bus.read_byte(INPUT_PAR['adc_addr'])
    
    def get_ext_states(self):
        t0 = time.time()
        ext_state_samples = np.zeros((1, len(INPUT_PAR['ext_state_vars'])), dtype=np.uint8)
        
        while (time.time() - t0 < INPUT_PAR['period']):
            sample = np.array([
                (self.button_1).value, 
                (self.button_2).value, 
                GPIO.input(INPUT_PAR['boop']), 
                1 if (self.bus).read_byte(INPUT_PAR['adc_addr']) > INPUT_PAR['adc_th'] else 0]).reshape(1,-1)
            
            ext_state_samples = np.concatenate((ext_state_samples, sample), axis=0)

            time.sleep(INPUT_PAR['samp_int'])

        ext_states_lst = []
        for col in range(len(INPUT_PAR['ext_state_vars'])):
            samples = ext_state_samples[1:,col]
            differ = np.diff(samples)
            pulse = np.flatnonzero(differ)
            
            if len(pulse) == 0:
                ext_states_lst.append(1 if samples[-1] == 1 else 0)
                continue
            
            voltage = np.split(samples, (pulse + 1))
            high_cnt = map(lambda x:len(x), voltage[1::2] if differ[pulse[0]] == 1 else voltage[::2])
            ext_states_lst.append(1 if max(high_cnt) >= INPUT_PAR['min_eff_len'] else 0)
        
        ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])

        return ext_states

    def closeall(self):
        (self.button_1).close()
        (self.button_2).close()
        GPIO.cleanup(INPUT_PAR['boop'])
        (self.bus).close()