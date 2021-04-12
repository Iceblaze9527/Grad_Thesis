import time

import numpy as np

import smbus
from gpiozero import Button
import RPi.GPIO as GPIO

ext_state_vars = ['FOOD', 'TOXIN', 'BOOP', 'PULL']

#FOOD: BUTTON
BUTTON_RED = 27
#TOXIN: BUTTON
BUTTON_YEL = 25
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

def get_ext_states():
    ##TODO: init (class needed)
    button_red = Button(pin=BUTTON_RED, pull_up=True)
    button_yel = Button(pin=BUTTON_YEL, pull_up=True)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TOUCH, GPIO.IN)

    bus = smbus.SMBus(1)
    bus.write_byte(ADDR,AIN0)
    bus.read_byte(ADDR)#

    t0 = time.time()
    ext_state_samples = np.zeros((1, len(ext_state_vars)), dtype=np.uint8)
    
    while (time.time() - t0 < TIME_LIMIT):
        sample = np.array([button_red.value, button_yel.value, GPIO.input(TOUCH), \
            1 if bus.read_byte(ADDR) > THRESHOLD else 0]).reshape(1,-1)
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

    #TODO: close and clean (class methods)
    button_red.close()
    button_yel.close()
    GPIO.cleanup(TOUCH)
    bus.close()
    
    return ext_states

if __name__ == '__main__':
    try:
        while True:
            x = get_ext_states()
            print(x)
            time.sleep(0.05)
    except KeyboardInterrupt:
        exit()