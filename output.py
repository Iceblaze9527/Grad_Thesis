from led import LEDEyes
from sound import SoundPlay

int_state_space = ['HAPPY', 'SAD', 'FEAR', 'ANGRY']

LED_ROW        = 5       # Row of LED pixels
LED_COL        = 5       # Column of LED pixels
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 15      # Set to 0 for darkest and 255 for brightest
LED_CHANNEL    = 0       # PWM channel index

PERIOD = 3 #seconds

PATH = '/home/pi/sounds'
WAV_HAPPY = 'happy-1.wav'
WAV_SAD = 'sad-1.wav'
WAV_FEAR = 'fear-1.wav'
WAV_ANGRY = 'angry-1.wav'

# ctrl.send_action_signal() in rl branch: get action signal and acts accordingly
# init and if-else
# done within 3 secs
# ready, success and fail cmd?
# _cleanup() method

def send_action_command(action):
    sound_happy = SoundPlay(PATH, WAV_HAPPY)
    sound_sad = SoundPlay(PATH, WAV_SAD)
    sound_fear = SoundPlay(PATH, WAV_FEAR)
    sound_angry = SoundPlay(PATH, WAV_ANGRY)
    
    led = LEDEyes(LED_ROW, LED_COL, PERIOD, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    
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

send_action_command(0)
