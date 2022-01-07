import sys, time, machine, uos, random, gc
import ftext
from time import sleep
import picodisplay as disp
from machine import Pin, ADC
from ulab import numpy as np
gc.collect()

# Initialise Picodisplay with a bytearray display buffer
buf = bytearray(disp.get_width() * disp.get_height() * 2)

disp.init(buf)
disp.set_backlight(1.0)
disp.set_pen(0, 0, 0)                    
disp.clear()                               
disp.update()

disp.set_pen(255, 255, 255)  
font_file = "/fonts/uppmat.fnt"
#ftext.displine(disp,0,0,100,100)
t1 = time.ticks_ms()
#ftext.text(disp, font_file, "SCOTTIE :",32,0)
ftext.text(disp, font_file, "PI = 3.14",0,32,0.2)
ftext.text(disp, font_file, '\x70SIN(X)=-COS',0,80)
t2 = time.ticks_ms()
print(t2-t1)
disp.update()
disp.set_pen(0, 0, 0) 
disp.clear()
disp.set_pen(255, 255, 255)  
disp.update()
row = 0
for scale in list(np.arange(0.2,1.4,0.2)):
    row += int(28*scale)
    print(scale)
    ftext.text(disp, font_file, "SCOTTIE",0,row,scale)
disp.update()
#disp.set_pen(255, 255, 255)                # Set a white pen
#disp.text("Scottie", 10, 10, 240, 6)  # Add some text
