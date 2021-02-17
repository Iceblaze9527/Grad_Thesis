# -*- coding: UTF-8 -*-
#import chardet
import os
import time
import logging

import spidev
from PIL import Image,ImageDraw,ImageFont

from lib.waveshare_LCD2inch4 import LCD_2inch4

# pin configuration (SPI1)
RST = 26
DC = 6
BL = 16
BUS = 1 
DEV = 1 

root_path = '/home/pi'
img_name = 'test.png'#or .jpg

img_path = os.path.join(root_path, img_name)
logging.basicConfig(level=logging.INFO)

try:
    ''' Warning!!!Don't create multiple displayer objects!!! '''
    disp = LCD_2inch4.LCD_2inch4(spi=spidev.SpiDev(BUS,DEV), rst=RST, dc=DC, bl=BL)#spi_freq=40000000, bl_freq=1000, i2c=None,i2c_freq=100000
    disp.Init()# Initialize library.
    disp.clear()# Clear display.
    
    image = Image.open(img_path)
    image = image.rotate(0)
    disp.ShowImage(image)
    logging.info("show image")
    
    time.sleep(3)
    
    disp.module_exit()
    logging.info("quit:")

except IOError as e:
    logging.info(e)    

except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()