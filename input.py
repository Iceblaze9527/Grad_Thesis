import time
from gpiozero import Button

INT = 1

button_red = Button(pin=24, pull_up=True)##bcm code
button_yel = Button(pin=27, pull_up=True)

while True:
    time.sleep(INT)
    print(button_red.is_pressed)
    print(button_yel.is_pressed)