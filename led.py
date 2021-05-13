import time
from rpi_ws281x import Adafruit_NeoPixel

class LEDEyes():
	def __init__(self, period, led_row, led_col, *args):
		self.period = period
		self.led_row = led_row
		self.led_col = led_col
		self.strip = Adafruit_NeoPixel(led_row*led_col, *args)
		(self.strip).begin()

	def happy_eyes(self, steps, blink, diff):
		_red_func = lambda intensity, row: int(intensity * diff if (row in [0,self.led_row-1]) else 0)
		_green_func = lambda intensity, row: int(0xff - intensity * diff)
		_blue_func = lambda intensity, row: 0x00

		rounds = steps // blink
		half = rounds // 2
		interval = self.period / steps
		
		for step in range(steps):
			ratio = ((step % rounds) / half) if ((step % rounds) < half + 1) else ((rounds - (step % rounds)) / half)
			
			for i in range(self.led_row):
				_red = _red_func(ratio, i)
				_green = _green_func(ratio, i)
				_blue = _blue_func(ratio, i)

				_rgb = int((_red << 16) | (_green << 8) | _blue)
				
				for j in range(self.led_col):
					(self.strip).setPixelColor(j + self.led_col * i, _rgb)
			
			(self.strip).show()
			time.sleep(interval)

	def sad_eyes(self, steps, diff):
		_red_func = lambda intensity: 0x00
		_green_func = lambda intensity: 0x00
		_blue_func = lambda intensity: int(0xff - intensity * diff)
		
		interval = self.period / steps
		
		for step in range(steps):
			ratio = step / steps
			
			_red = _red_func(ratio)
			_green = _green_func(ratio)
			_blue = _blue_func(ratio)
			
			_rgb = int((_red << 16) | (_green << 8) | _blue)
			
			for i in range((self.strip).numPixels()):
				(self.strip).setPixelColor(i, _rgb)
			
			(self.strip).show()
			time.sleep(interval)


	def fear_eyes(self, steps, diff, width):
		_jitt = lambda col, low_lst: diff if col in low_lst else 0

		_red_func = lambda step, jitt: 0xff - jitt
		_green_func = lambda step, jitt: 0xff - jitt
		_blue_func = lambda step, jitt: 0x00

		low_lst = range(2 * width)
		interval = self.period / steps
		
		for step in range(steps):
			low_lst = [(self.led_col - 1) if col == 0 else col - 1 for col in low_lst] if (step % (4 * width)) < (2 * width) \
				else [0 if col == (self.led_col - 1) else col + 1 for col in low_lst]

			for j in range(self.led_col):
				_red = _red_func(step, _jitt(j, low_lst))
				_green = _green_func(step, _jitt(j, low_lst))
				_blue = _blue_func(step, _jitt(j, low_lst))
				
				_rgb = int((_red << 16) | (_green << 8) | _blue)
				
				for i in range(self.led_row):
					(self.strip).setPixelColor(j + self.led_col * i, _rgb)
			
			(self.strip).show()
			time.sleep(interval)

	def angry_eyes(self, steps, diff):
		_red_func = lambda step, differ: int(0xff - differ)
		_green_func = lambda step, differ: 0x00
		_blue_func = lambda step, differ: 0x00
		
		interval = self.period / steps
		
		for step in range(steps):
			differ = diff if (step % 2) == 1 else 0
			
			_red = _red_func(step, differ)
			_green = _green_func(step, differ)
			_blue = _blue_func(step, differ)
			
			_rgb = int((_red << 16) | (_green << 8) | _blue)
			
			for i in range((self.strip).numPixels()):
				(self.strip).setPixelColor(i, _rgb)
			
			(self.strip).show()
			time.sleep(interval)
		
	def success_eyes(self):
		pass
	def fail_eyes(self):
		pass