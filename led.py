import time
import random
from rpi_ws281x import Adafruit_NeoPixel, Color

LED_COUNT      = 25      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

PERIOD = 3 #seconds

def sad_eyes(strip_inst, steps):
	red_func = lambda step: 0x00
	green_func = lambda step: 0x00
	blue_func = lambda step: int(0xff - step)
	
	num = strip_inst.numPixels()
	interval = PERIOD / steps
	
	for step in range(steps):
		_red = red_func(step)
		_green = green_func(step)
		_blue = blue_func(step)
		
		_rgb = int((_red << 16) | (_green << 8) | _blue)
		
		for i in range(0, num):
			strip_inst.setPixelColor(i, _rgb)
		
		strip_inst.show()##
		time.sleep(interval)


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

try:
	# while True:
	strip.begin()
	sad_eyes(strip, 223)
except KeyboardInterrupt:
	exit()
	
	
	# #Reverse order	
	# for i in range(0,strip.numPixels()):
	# 	strip.setPixelColor(strip.numPixels()-i, Color(0,255,0))	
	# 	strip.show()
	# 	time.sleep(0.05)
	# #Turn around
	# for i in range(0,strip.numPixels()//4):
	# 	strip.setPixelColor(i, Color(255,0,0))
	# 	strip.show()
	# 	time.sleep(0.05)
	# for i in range(0,strip.numPixels()//8-1):
	# 	strip.setPixelColor(7+8*i, Color(255,0,0))	
	# 	strip.show()
	# 	time.sleep(0.05)
	# for i in range(0,strip.numPixels()//4+1):
	# 	strip.setPixelColor(strip.numPixels()-i, Color(255,0,0))
	# 	strip.show()
	# 	time.sleep(0.05)
	# for i in range(0,strip.numPixels()//8-1):
	# 	strip.setPixelColor(16-8*i, Color(255,0,0))	
	# 	strip.show()
	# 	time.sleep(0.05)	
	# for i in range(0,strip.numPixels()//4-1):
	# 	strip.setPixelColor(i+8, Color(255,0,0))	
	# 	strip.show()
	# 	time.sleep(0.05)		
	# for i in range(0,strip.numPixels()//4-1):
	# 	strip.setPixelColor(strip.numPixels()-9-i, Color(255,0,0))	
	# 	strip.show()
	# 	time.sleep(0.05)	
	
	# #Middle to both sides, both sides to the middle
	# for i in range(0,strip.numPixels()//4-1):
	# 	for y in range(0,strip.numPixels()//8):
	# 		strip.setPixelColor(4+y*8+i, Color(0,255,255))
	# 		strip.setPixelColor(3+y*8-i, Color(0,255,255))
	# 	strip.show()
	# 	time.sleep(0.1)
	# for i in range(0,strip.numPixels()//4-1):
	# 	for y in range(0,strip.numPixels()//8):
	# 		strip.setPixelColor(7+y*8-i, Color(255,255,0))
	# 		strip.setPixelColor(y*8+i, Color(255,255,0))
	# 	strip.show()
	# 	time.sleep(0.1)
	# #random color
	# for x in range(0,5):
	# 	for i in range(0,strip.numPixels()):
	# 		strip.setPixelColor(i, Color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))	
	# 		strip.show()
	# 	time.sleep(0.5)