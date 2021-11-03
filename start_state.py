import Framework
from pico2d import *
import main
import select_state
img = None

def init():
    global img
    Framework.running = True
    img = load_image('./img/start_img.png')

def exit():
    print("start exit")
    global img
    del(img)
    

def handle_events():
    events = get_events()
    for event in events:
        if(event.type == SDL_MOUSEBUTTONDOWN):
            print("click")
            Framework.chstate(select_state)
        if event.type == SDL_QUIT:
           quit()

def draw():
    clear_canvas()
    img.draw_to_origin(0, 0)
    update_canvas()


def update():
    pass



