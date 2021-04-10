import os
import time

import simpleaudio as simpad
from rpi_ws281x import Adafruit_NeoPixel

import led, sound

LED_COUNT      = 25      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 15    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

root_path = '/home/pi'
wav_name = 'rodent.wav'

if __name__ == '__main__':
    wav_path = os.path.join(root_path, wav_name)
    wav_obj = simpad.WaveObject.from_wave_file(wav_path)
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    try:
        play_obj = sound.play_audio(wav_obj)
        strip.begin()
        
        led.happy_eyes(strip, 50, 2, 192)
        led.sad_eyes(strip, 50, 192)
        led.fear_eyes(strip, 25, 192, 1)
        led.angry_eyes(strip, 25, 192)
        # time.sleep(1.5)
        
        strip._cleanup()
        sound.stop_audio(play_obj)
    except KeyboardInterrupt:
        strip._cleanup()
        exit()
