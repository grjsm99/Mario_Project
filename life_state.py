import Framework
from pico2d import *
import main

img = None
num_img = None
logo_time = None

def init():
    global img
    global num_img
    global logo_time
    logo_time = 0
    img = load_image('./img/life_s.png')
    num_img = load_image('./img/num.png')
    Framework.life -= 1

def exit():
    print("life exit")
    global img
    del(img)
    

def handle_events():
    pass

def draw():
    clear_canvas()
    img.draw_to_origin(0, 0)
    num_img.clip_draw(Framework.life * 16, 0, 16, 16, 540, 370)
    update_canvas()


def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0        
        Framework.chstate(main)
    delay(0.01)
    logo_time += 0.01




