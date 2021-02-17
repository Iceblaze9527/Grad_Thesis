import os
import sys 
import time
import logging

import spidev
from PIL import Image,ImageDraw,ImageFont

from lib.waveshare_LCD2inch4 import LCD_2inch4

RST_L = 27
DC_L = 25
BL_L = 18
BUS_L = 0
DEV_L = 0

RST_R = 26
DC_R = 6
BL_R = 16
BUS_R = 1
DEV_R = 1

root_path = '/home/pi'
img_name_l = 'test.png'
img_name_r = 'test.jpg'

img_path_l = os.path.join(root_path, img_name_l)
img_path_r = os.path.join(root_path, img_name_r)

logging.basicConfig(level=logging.INFO)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't create multiple displayer objects!!! '''
    disp_l = LCD_2inch4.LCD_2inch4(spi=spidev.SpiDev(BUS_L,DEV_L), rst=RST_L, dc=DC_L, bl=BL_L, spi_freq=40000000)
    disp_l.Init()
    disp_l.clear()
    
    disp_r = LCD_2inch4.LCD_2inch4(spi=spidev.SpiDev(BUS_R,DEV_R), rst=RST_R, dc=DC_R, bl=BL_R, spi_freq=40000000)
    disp_r.Init()
    disp_r.clear()

    image_l = Image.open(img_path_l)
    image_l = image_l.rotate(0)
    disp_l.ShowImage(image_l)
    logging.info("show left image")
    
    image_r = Image.open(img_path_r)
    image_r = image_r.rotate(0)
    disp_r.ShowImage(image_r)
    logging.info("show right image")
    
    disp_l.clear()
    disp_r.clear()
    disp_l.ShowImage(image_r)
    disp_r.ShowImage(image_l)
    
    time.sleep(3)
    disp_l.module_exit()
    logging.info("quit left")
    
    disp_r.module_exit()
    logging.info("quit right")

except IOError as e:
    logging.info(e)    

except KeyboardInterrupt:
    time.sleep(3)
    disp_l.module_exit()
    logging.info("quit left")
    
    disp_r.module_exit()
    logging.info("quit right")
    exit()