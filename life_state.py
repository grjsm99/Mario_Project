import Framework
from pico2d import *
import main

img = None

def init():
    global img
    print("!")
    img = load_image('./img/kpu_credit.png')

def exit():
    pass

def handle_events():
    pass

def draw():
    img.clip_draw(0, 0, 500, 500, 0, 0)

def update():
    pass




