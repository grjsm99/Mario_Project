import Framework
from pico2d import *
import main

img = None
logo_time = None

def init():
    global img
    global logo_time
    Framework.running = True
    logo_time = 0
    img = load_image('./img/kpu_credit.png')

def exit():
    global img
    del(img)
    

def handle_events():
    pass

def draw():
    clear_canvas()
    img.draw(400, 300)
    update_canvas()


def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0        
        Framework.chstate(main)
    delay(0.01)
    logo_time += 0.01




