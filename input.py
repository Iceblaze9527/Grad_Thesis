import time

import numpy as np

import smbus
from gpiozero import Button
import RPi.GPIO as GPIO

ext_state_vars = ['FOOD', 'TOXIN', 'BOOP', 'PULL']

#FOOD: BUTTON
BUTTON_RED = 27
#TOXIN: BUTTON
BUTTON_YEL = 22
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
    t0 = time.time()
    ## init
    ext_state_samples = np.zeros(1, len(ext_state_vars), dtype=np.uint8)

    button_red = Button(pin=BUTTON_RED, pull_up=True)
    button_yel = Button(pin=BUTTON_YEL, pull_up=True)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TOUCH, GPIO.IN)
    
    bus = smbus.SMBus(1)
    bus.write_byte(ADDR,AIN0)
    bus.read_byte(ADDR)#
    
    while (time.time() - t0 < TIME_LIMIT):
        sample = np.array([button_red.value, button_yel.value, GPIO.input(TOUCH), \
            1 if bus.read_byte(ADDR) > THRESHOLD else 0]).reshape(1,-1)
        ext_state_samples = np.concatenate((ext_state_samples, sample), axis=0)

        time.sleep(SAMPLE_INTERVAL)
    
    ext_states_lst = np.where(np.count_nonzero(ext_state_samples, axis=0) > MIN_EFF_INPUT_LEN, 1, 0)
    ext_states = sum([state << index for index, state in enumerate(ext_states_lst)])#return
    
    GPIO.cleanup(TOUCH)
    
    return ext_states