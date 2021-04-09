import time
import random
from rpi_ws281x import Adafruit_NeoPixel, Color

LED_COUNT      = 25      # Number of LED pixels.
LED_ROW        = 5       # Row of LED pixels
LED_COL        = 5       # Column of LED pixels

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
		
		for i in range(num):
			strip_inst.setPixelColor(i, _rgb)
		
		strip_inst.show()
		time.sleep(interval)


def fear_eyes(strip_inst, steps, diff, width):
	jitt = lambda row, low_lst: diff if row in low_lst else 0

	red_func = lambda step, jitt: 0xff - jitt
	green_func = lambda step, jitt: 0xff - jitt
	blue_func = lambda step, jitt: 0x00

	n = 4 * width
	low_lst = range(2 * width)
	interval = PERIOD / steps
	
	for step in range(steps):
		if (step % n) < (2 * width):
			low_lst = [(row - 1) for row in low_lst]
			low_lst = [(LED_ROW - 1) if row == -1 else row for row in low_lst]
		else:
			low_lst = [(row + 1) for row in low_lst]
			low_lst = [0 if row == LED_ROW else row for row in low_lst]

		for i in range(LED_ROW):
			_red = red_func(step, jitt(i, low_lst))
			_green = green_func(step, jitt(i, low_lst))
			_blue = blue_func(step, jitt(i, low_lst))
			
			_rgb = int((_red << 16) | (_green << 8) | _blue)
			
			for j in range(LED_COL):
				strip_inst.setPixelColor(j+5*i, _rgb)
		
		strip_inst.show()
		time.sleep(interval)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

try:
	strip.begin()
	# sad_eyes(strip, 223)
	fear_eyes(strip, 80, 192, 1)
	strip._cleanup()
except KeyboardInterrupt:
	strip._cleanup()
	exit()
	
	
	# #Reverse order	

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