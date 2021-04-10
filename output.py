from led import LEDEyes
from sound import SoundPlay

LED_ROW        = 5       # Row of LED pixels
LED_COL        = 5       # Column of LED pixels
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 15    # Set to 0 for darkest and 255 for brightest

PERIOD = 3 #seconds

PATH = '/home/pi/sounds'
WAV_HAPPY = 'happy-1.wav'
WAV_SAD = 'sad-1.wav'
WAV_FEAR = 'fear-1.wav'
WAV_ANGRY = 'angry-1.wav'

if __name__ == '__main__':
    sound_happy = SoundPlay(PATH, WAV_HAPPY)
    sound_sad = SoundPlay(PATH, WAV_SAD)
    sound_fear = SoundPlay(PATH, WAV_FEAR)
    sound_angry = SoundPlay(PATH, WAV_ANGRY)
    
    led = LEDEyes(LED_ROW, LED_COL, PERIOD, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    
    try:
        sound_happy.play()
        led.happy_eyes(50, 2, 192)
        sound_happy.stop()

        sound_sad.play()
        led.sad_eyes(50, 192)
        sound_sad.stop()
        
        sound_fear.play()
        led.fear_eyes(25, 192, 1)
        sound_fear.stop()

        sound_angry.play()
        led.angry_eyes(25, 192)
        sound_angry.stop()
    except KeyboardInterrupt:
        exit()
