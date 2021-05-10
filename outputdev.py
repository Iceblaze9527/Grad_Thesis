import time

from led import LEDEyes
from sound import SoundPlay

# TODO: ready, success and fail cmd?
# TODO: param.py

action_space = ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK']
PATH = '/home/pi/sounds'
WAV_FILES = ['happy-1.wav', 'sad-1.wav', 'fear-1.wav', 'angry-1.wav']

LED_ROW        = 4       # Row of LED pixels
LED_COL        = 8       # Column of LED pixels
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 15      # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel index

PERIOD = 3 #seconds

class OutputDevices():
    def __init__(self):
        self.led = LEDEyes(LED_ROW, LED_COL, PERIOD, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    def exec_action(self, action):
        sound = SoundPlay(PATH, WAV_FILES[action])
        
        sound.play()
        if action_space[action] == 'HAP_LOOK':
            (self.led).happy_eyes(50, 2, 128)
        elif action_space[action] == 'SAD_LOOK':
            (self.led).sad_eyes(50, 192)
        elif action_space[action] == 'FEA_LOOK':
            (self.led).fear_eyes(25, 192, 1)
        elif action_space[action] == 'ANG_LOOK':
            (self.led).angry_eyes(25, 192)
        sound.stop()
    
    def closeall(self):
        (self.led.strip)._cleanup()

if __name__ == '__main__':
    try:
        outputs = OutputDevices()
        for i in range(len(action_space)):
            outputs.exec_action(i)
            time.sleep(1)
    except KeyboardInterrupt:
        outputs.closeall()
        exit()
