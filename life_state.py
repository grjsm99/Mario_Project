import Framework
from pico2d import *
import main
import select_state

img = None
num_img = None
logo_time = None
stage = 1
state_type = 0
def init():
    global img
    global num_img
    global logo_time
    logo_time = 0
    num_img = load_image('./img/num.png')

    if state_type == 0:
        Framework.life -= 1
        if Framework.life>0:
            img = load_image('./img/life_s.png')
        else:
            img = load_image('./img/gover.png')
    else:
        logo_time -= 1
        select_state.roundclear[Framework.selectStage+1] = 30
        img = load_image('./img/clear.png')

def exit():
    print("life exit")
    global img
    del(img)
    

def handle_events():
    pass

def draw():
    clear_canvas()
    img.draw_to_origin(0, 0)
    if(Framework.life>0 and state_type == 0):
        num_img.clip_draw(Framework.life * 16, 0, 16, 16, 540, 370)
    update_canvas()


def update():
    global logo_time
    if (logo_time > 1.0):
        if state_type == 0:
            if Framework.life>0:
                logo_time = 0        
                Framework.chstate(main)
            else:   
                quit()
        else:
            logo_time = 0
            Framework.chstate(select_state)
        
    delay(0.01)
    logo_time += 0.01




