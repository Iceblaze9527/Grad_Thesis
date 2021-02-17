from gpiozero import Button
import time

INT = 1

button = Button(pin=18, pull_up=True)

while True:
    time.sleep(INT)
    print(button.is_pressed)