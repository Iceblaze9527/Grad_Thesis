import smbus
import time

import RPi.GPIO as GPIO
from gpiozero import Button

# CHANNEL = 24
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(CHANNEL, GPIO.IN)

# print(GPIO.input(CHANNEL))

address = 0x48
AIN0 = 0x00
AIN1 = 0x01

bus = smbus.SMBus(1)

try:
    bus.write_byte(address,AIN0)
    bus.read_byte(address)#第一次空读
    while True:
        bus.write_byte(address,AIN0)
        x_val = bus.read_byte(address)
        print('x:', x_val)
        
        bus.write_byte(address,AIN1)
        y_val = bus.read_byte(address)
        print('y:', y_val)
        
        print('----')
        time.sleep(1)
except KeyboardInterrupt:
    exit()

# button_red = Button(pin=24, pull_up=True)##bcm code
# button_yel = Button(pin=27, pull_up=True)

# print(button_red.is_pressed)
# print(button_yel.is_pressed)