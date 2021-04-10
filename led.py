import time

LED_ROW        = 5       # Row of LED pixels
LED_COL        = 5       # Column of LED pixels

PERIOD = 3 #seconds

class LEDEyes():
	def __init__(self):
		pass

def happy_eyes(strip_inst, steps, blink, diff):
	red_func = lambda intensity, col: int(intensity * diff if (col in [0,LED_COL-1]) else 0)
	green_func = lambda intensity, col: int(0xff - intensity * diff)
	blue_func = lambda intensity, col: 0x00

	rounds = steps // blink
	half = rounds // 2
	interval = PERIOD / steps
	
	for step in range(steps):
		ratio = ((step % rounds) / half) if ((step % rounds) < half + 1) else ((rounds - (step % rounds)) / half)
		
		for j in range(LED_COL):
			_red = red_func(ratio, j)
			_green = green_func(ratio, j)
			_blue = blue_func(ratio, j)

			_rgb = int((_red << 16) | (_green << 8) | _blue)
			
			for i in range(LED_ROW):
				strip_inst.setPixelColor(j+5*i, _rgb)
		
		strip_inst.show()
		time.sleep(interval)

def sad_eyes(strip_inst, steps, diff):
	red_func = lambda intensity: 0x00
	green_func = lambda intensity: 0x00
	blue_func = lambda intensity: int(0xff - intensity * diff)
	
	num = strip_inst.numPixels()
	interval = PERIOD / steps
	
	for step in range(steps):
		ratio = step / steps
		
		_red = red_func(ratio)
		_green = green_func(ratio)
		_blue = blue_func(ratio)
		
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

	low_lst = range(2 * width)
	interval = PERIOD / steps
	
	for step in range(steps):
		low_lst = [(LED_ROW - 1) if row == 0 else row - 1 for row in low_lst] if (step % (4 * width)) < (2 * width) \
			else [0 if row == (LED_ROW - 1) else row + 1 for row in low_lst]

		for i in range(LED_ROW):
			_red = red_func(step, jitt(i, low_lst))
			_green = green_func(step, jitt(i, low_lst))
			_blue = blue_func(step, jitt(i, low_lst))
			
			_rgb = int((_red << 16) | (_green << 8) | _blue)
			
			for j in range(LED_COL):
				strip_inst.setPixelColor(j+5*i, _rgb)
		
		strip_inst.show()
		time.sleep(interval)

def angry_eyes(strip_inst, steps, diff):
	red_func = lambda step, differ: int(0xff - differ)#
	green_func = lambda step, differ: 0x00
	blue_func = lambda step, differ: 0x00
	
	num = strip_inst.numPixels()
	interval = PERIOD / steps
	
	for step in range(steps):
		differ = diff if (step % 2) == 1 else 0
		
		_red = red_func(step, differ)
		_green = green_func(step, differ)
		_blue = blue_func(step, differ)
		
		_rgb = int((_red << 16) | (_green << 8) | _blue)
		
		for i in range(num):
			strip_inst.setPixelColor(i, _rgb)
		
		strip_inst.show()
		time.sleep(interval)

# if __name__ == '__main__':
# 	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# 	try:
# 		strip.begin()
# 		happy_eyes(strip, 50, 2, 192)
# 		sad_eyes(strip, 50, 192)
# 		fear_eyes(strip, 25, 192, 1)
# 		angry_eyes(strip, 25, 192)
# 		strip._cleanup()
# 	except KeyboardInterrupt:
# 		strip._cleanup()
# 		exit()