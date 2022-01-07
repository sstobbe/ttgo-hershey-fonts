import sys, time, machine, uos, random, gc
from time import sleep
import picodisplay as disp
from machine import Pin, ADC

sys.path.append('/pyfonts')
import uppmat
import pytext

gc.collect()

# Initialise Picodisplay with a bytearray display buffer
buf = bytearray(disp.get_width() * disp.get_height() * 2)

disp.init(buf)
disp.set_backlight(1.0)
disp.set_pen(0, 0, 0)                    
disp.clear()                               
disp.update()

disp.set_pen(255, 255, 255)  
t1 = time.ticks_ms()
pytext.text(disp, uppmat, "SCOTTIE :",32,0)
pytext.text(disp, uppmat, '\x70SIN(X)=-COS',80,0)
t2 = time.ticks_ms()
print(t2-t1)
disp.update()