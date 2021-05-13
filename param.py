INPUT_PAR = {
    'ext_state_vars':['FOOD', 'TOXIN', 'BOOP', 'PULL'],
    'button_food':27,
    'button_toxin':25,
    'boop':23,
    'adc_addr':0x48,
    'adc_ain0':0x00,
    'adc_th':192,
    'period':5,# in seconds
    'samp_int':0.1,# in seconds
    'min_eff_len':10# samples
}

OUTPUT_PAR = {
    'action_space': ['HAP_LOOK', 'SAD_LOOK', 'FEA_LOOK', 'ANG_LOOK', 'SUCCESS', 'FAIL'],
    'wav_path': '/home/pi/sounds',
    'wav_files': ['happy-1.wav', 'sad-1.wav', 'fear-1.wav', 'angry-1.wav', 'happy-2.wav', 'sad-2.wav'],
    'period': 3,# in seconds
    'led': {
        'LED_ROW': 4,# Row of LED pixels
        'LED_COL': 8,# Column of LED pixels
        'LED_PIN': 18,# GPIO pin connected to the pixels (must support PWM!)
        'LED_FREQ_HZ': 800000,# LED signal frequency in hertz (usually 800khz)
        'LED_DMA': 5,# DMA channel to use for generating signal (try 5)
        'LED_INVERT': False,# True to invert the signal (when using NPN transistor level shift)
        'LED_BRIGHTNESS': 15,# Set to 0 for darkest and 255 for brightest
        'LED_CHANNEL': 0# PWM channel index
    }
}