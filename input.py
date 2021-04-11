import time

from gpiozero import Button
import RPi.GPIO as GPIO
import smbus

BUTTON_RED = 27
BUTTON_YEL = 22
TOUCH = 23

ADDR = 0x48
AIN0 = 0x00
AIN1 = 0x01

# ctrl.get_ext_states() in rl branch: get the external state code when called
# default input values are all set to False(0)
# within a time limit (e.g. 1s), scan and sample all input ports (we can get hundreds approx.)
# check effective inputs (i.e. filter illegal inputs) (criteria? time costs?)
# return input values when exceeding time limits (countdown methods?)

if __name__ == '__main__':
    button_red = Button(pin=BUTTON_RED, pull_up=True)
    button_yel = Button(pin=BUTTON_YEL, pull_up=True)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TOUCH, GPIO.IN)
    
    bus = smbus.SMBus(1)
    bus.write_byte(ADDR,AIN0)
    bus.read_byte(ADDR)#
   
    try:
        while True:
            print('red:', button_red.is_pressed)
            print('yellow:', button_yel.is_pressed)
            
            print('touch:', GPIO.input(TOUCH))
            
            bus.write_byte(ADDR,AIN0)
            x_val = bus.read_byte(ADDR)
            print('joy_x:', x_val)

            bus.write_byte(ADDR,AIN1)
            y_val = bus.read_byte(ADDR)
            print('joy_y:', y_val)
            
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup(TOUCH)
        exit()