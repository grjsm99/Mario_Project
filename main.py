from pico2d import *
from mario import Mario
from Mob import Mob
from Framework import *
from maptile2 import Mapset
from maptile2 import Moblist
from frac import Frac
import math


BLOCK_TYPES = 8
MOB_TYPES = 2
MW, MH = 1024, 768

bimglist = None
Tilelist = None
map_bg = None
fimg = None
camPos = None
backPos = None
fraclist = None
chr = None
isRight = None
isLeft = None
isLeftMove = None
mimglist = None
Tilelist = None
Moblist_ = None
def init():

    global mimglist
    global bimglist
    global map_bg
    global fimg
    global fraclist
    global camPos
    global backPos
    global chr
    global running
    global isRight
    global isLeft
    global isLeftMove
    global Tilelist
    global Moblist_
    Tilelist = Mapset
    Moblist_ = Moblist
    map_bg = load_image('./img/bg.jpg')
    fimg = load_image('./img/frac.png')
    bimglist = []
    fraclist = []
    mimglist = []
    for i in range(BLOCK_TYPES):
        bimglist.append(load_image("./img/b%d.png" % i))
    for i in range(MOB_TYPES):
        mimglist.append(load_image("./img/m%d.png" % i))

    camPos = 0
    backPos = 0

    chr = Mario()
 
    running = True
    isRight = False
    isLeft = False
    isLeftMove = False

def handle_events():
    global running  
    global isRight
    global isLeft
    global isLeftMove
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            pass
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                isRight = True
                isLeftMove = False
            if event.key == SDLK_LEFT:
                isLeft = True
                isLeftMove = True
            if event.key == SDLK_UP:
                chr.chuplook(1)
            if event.key == SDLK_DOWN:
                chr.chuplook(2)
            if event.key == SDLK_SPACE and chr.isjump == False:
                chr.jump(8.3)
            if event.key == SDLK_a:
                chr.eat_Mushroom()  
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                isRight = False   
            if event.key == SDLK_LEFT:
                isLeft = False
            if event.key == SDLK_UP:
                chr.chuplook(0)
                chr.resetMotion()
            if event.key == SDLK_DOWN:
                chr.chuplook(0)
                chr.resetMotion()
            elif event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                chr.setfric()
        if event.type == SDL_QUIT:
            quit()

def draw():
    clear_canvas()
    map_bg.draw(MW // 2 - backPos, MH // 2)
    map_bg.draw(MW // 2 - backPos + MW, MH // 2)
    draw_tileset()

    if chr.isMushAni == True:
        chr.mush_Ani()

    else:    
        chr.motionUpdate(Tilelist)
        for i in range(len(Moblist_)):
            Moblist_[i].motionUpdate(Tilelist)
    draw_mob()
    chr.draw()
    update_canvas()

def draw_mob():
    for i in range(len(Moblist_)):
        if Moblist_[i].xsp > 0:
            mimglist[Moblist_[i].type].clip_draw(Moblist_[i].motion * 32, 0, 32, Moblist_[i].height, Moblist_[i].xpos+16-camPos, Moblist_[i].ypos+Moblist_[i].height/2)
        elif Moblist_[i].xsp < 0:
            mimglist[Moblist_[i].type].clip_composite_draw(Moblist_[i].motion * 32, 0, 32, Moblist_[i].height, 0, 'h', Moblist_[i].xpos+16-camPos, Moblist_[i].ypos+Moblist_[i].height/2, Moblist_[i].width, Moblist_[i].height)
        draw_rectangle(Moblist_[i].xpos - camPos, Moblist_[i].ypos, Moblist_[i].xpos - camPos + 32, Moblist_[i].ypos + Moblist_[i].height)

def draw_tileset():
    global camPos
    global fimg
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - camPos >= 0 and Tilelist[i].hbleft - camPos <= MW:
            if Tilelist[i].dl == True:
                draw_frac(Tilelist[i])
                del Tilelist[i]
                break
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - camPos >= 0 and Tilelist[i].hbleft - camPos <= MW:
           
            Tilelist[i].ani()
            bimglist[Tilelist[i].sptype].clip_draw(Tilelist[i].frame * 32, 0, 32, 32, Tilelist[i].hbleft + 16 - camPos, Tilelist[i].hbdown + 16)

    if len(fraclist) > 0: # 조각 그리기
        for i in range(len(fraclist)): 
            if fraclist[i].y < -16:
                del fraclist[i]
                return
            x, y = fraclist[i].rtxy()
            fimg.draw(x - camPos, y)
    
        

def draw_frac(t):
    global fraclist
    cx = t.hbleft + 16
    cy = t.hbup + 16

    fraclist.append(Frac(cx, cy, -2, 1))
    fraclist.append(Frac(cx, cy, -2, 2))
    fraclist.append(Frac(cx, cy, 2, 1))
    fraclist.append(Frac(cx, cy, 2, 2))


def update():
    global camPos
    camPos = chr.rtView()
    
    for i in range(len(Moblist_)):
        Moblist_[i].camPos = camPos
    if isRight == True and isLeft == True:
        pass
    elif isRight == True:
        chr.xyrun(0, 3) 
    elif isLeft == True:
        chr.xyrun(0, -3)
    else:
        chr.xyrun(0,0)
    backPos = camPos
    backPos %= MW

    for i in range(len(fraclist)): 
        fraclist[i].upd()
        #chr.xyrun(0,0)


    
#close_canvas()
