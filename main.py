from pico2d import *
from mario import Mario

from maptile2 import Mapset

import math


BLOCK_TYPES = 8


Tilelist = Mapset
MW, MH = 1024, 768

open_canvas(MW, MH)
from frac import Frac
map_bg = load_image('./img/bg.jpg')
fimg = load_image('./img/frac.png')
bimglist = []
fraclist = []
for i in range(BLOCK_TYPES):
    bimglist.append(load_image("./img/b%d.png" % i))


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
                print(len(fraclist))
            if event.key == SDLK_a:
                running = False
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
            running = False

def draw_tileset():
    global cmpPos
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - cmpPos >= 0 and Tilelist[i].hbleft - cmpPos <= MW:
            if Tilelist[i].dl == True:
                draw_frac(Tilelist[i])
                del Tilelist[i]
                break
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - cmpPos >= 0 and Tilelist[i].hbleft - cmpPos <= MW:
           
            Tilelist[i].ani()
            bimglist[Tilelist[i].sptype].clip_draw(Tilelist[i].frame * 32, 0, 32, 32, Tilelist[i].hbleft + 16 - cmpPos, Tilelist[i].hbdown + 16)

    if len(fraclist) > 0: # 조각 그리기
        for i in range(len(fraclist)): 
            if fraclist[i].y < -16:
                del fraclist[i]
                return
            fraclist[i].draw(cmpPos)
    
        

def draw_frac(t):
    global fraclist
    cx = t.hbleft + 16
    cy = t.hbup + 16
    print((cx, cy))
    fraclist.append(Frac(cx, cy, -2, 1))
    fraclist.append(Frac(cx, cy, -2, 2))
    fraclist.append(Frac(cx, cy, 2, 1))
    fraclist.append(Frac(cx, cy, 2, 2))


chr.eat_Mushroom()
while running:
    clear_canvas()
    cmpPos = chr.rtView()
    if isRight == True and isLeft == True:
        pass
    elif isRight == True:
        chr.xyrun(0, 3) 
    elif isLeft == True:
        chr.xyrun(0, -3)   
    backPos = cmpPos
    backPos %= MW
    map_bg.draw(MW // 2 - backPos, MH // 2)
    map_bg.draw(MW // 2 - backPos + MW, MH // 2)
    draw_tileset()


    chr.draw(Tilelist)
    chr.xyrun(0,0)
    update_canvas()

    handle_events()
    delay(0.01)
#close_canvas()
