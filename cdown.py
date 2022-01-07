# Happy New Year Countdown Tricket
#
# RPI Pico & Pimoroni Picodisplay (PIM543)
#
# Have Fun, -scottiebabe

import sys, time, machine, uos, random, gc
from time import sleep
import picodisplay as disp
from machine import Pin, ADC
import random
import hsv

# load the russhughes hershy font lib
import ftext
font_num = "/fonts/uppmat.fnt"
font_txt = "/fonts/scriptc.fnt"
font_sym = "/fonts/symbol.fnt"

gc.collect()

# Initialise Picodisplay with a bytearray display buffer
buf = bytearray(disp.get_width() * disp.get_height() * 2)

disp.init(buf)
disp.set_backlight(1.0)
disp.set_pen(0, 0, 0)                    
disp.clear()                               
disp.update()

# List of RGB tupples for star colors
starcolors = [ (255,255,0), (255,255,255), (0,245,255),(255,255,0), (255,225,255),
               (187,255,255),(255,228,225),(255,52,179),(255,236,139),(191,239,255),(255,105,180)]
# Create ST7789 Display Pens (16-bit R5G6B5 code)
starpens = [ disp.create_pen(*color) for color in starcolors]

# Set the new year to be 11 seconds from now
tend = time.time() + 11
td = tend - time.time()
tl = -1
scale = 4.0
cpen = 0
while td > 0:
    if td != tl:
        tl = td
        scale = 5.0
        cpen = disp.create_pen(*hsv.ToRGB(random.randint(0,359),1,1))
    else:
        scale = max(scale-0.2,1)
        
    disp.set_pen(0, 0, 0); disp.clear(); disp.set_pen(cpen)
    ftext.text(disp, font_num, "{}".format(td),80,80,scale)
    disp.update()
    td = tend - time.time()


star_y = [ random.randint(-50,0) for x in range(8) ]
star_v = [ random.randint(2,4) for x in range(8) ]
star_pen = [ random.choice(starpens) for x in range(8) ]

while disp.is_pressed(disp.BUTTON_A) == False:
    disp.set_pen(0, 0, 0); disp.clear(); disp.set_pen(255, 255, 255) 
    ftext.text(disp, font_txt, "Happy",50,60,1.8)
    ftext.text(disp, font_txt, "New Year!",10,120,1.5)
    ftext.text(disp, font_sym, "\x61",3,60,1.5)
    for i in range(0,8):
        x = 30*i
        disp.set_pen(star_pen[i])
        ftext.text(disp, font_sym, "\x4c",x,star_y[i],1.5)
        star_y[i] += star_v[i]
        if star_y[i] > 270:
            star_y[i] = random.randint(-50,0)
            star_pen[i] = random.choice(starpens)
    disp.update()