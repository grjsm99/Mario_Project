import Framework
from pico2d import *
import main

img = None
roundimg = None
rounddata = ((0, 30, 30, 173, 355), (0, 30, 30, 174, 517), (0, 30, 30, 421, 472), (0, 30, 30, 720, 368), (0, 30, 30, 787, 320))
roundclear = [30,30, 30, 30, 30]
def init():
    global img
    global roundimg
    Framework.running = True
    img = load_image('./img/lvselect.png')
    roundimg = load_image('./img/door.png')


def exit():
    print("select exit")
    global img
    del(img)
    

def handle_events():
    events = get_events()
    for event in events:
        if(event.type == SDL_MOUSEBUTTONDOWN):
            for i in range(len(rounddata)):
                if event.x >= rounddata[i][3] - 15 and event.x <= rounddata[i][3] + 15 and 768 - event.y >= rounddata[i][4] - 15 and 768 - event.y <= rounddata[i][4] + 15 and roundclear[i] == 30:
                    Framework.selectStage = i
                    Framework.chstate(main)
        if event.type == SDL_QUIT:
           quit()

def draw():
    clear_canvas()
    img.draw_to_origin(0, 0)
    for i in range(len(rounddata)):
        roundimg.clip_draw(roundclear[i], *rounddata[i])
    update_canvas()


def update():
    pass

