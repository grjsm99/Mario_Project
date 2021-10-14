from pico2d import *
from mario import Mario
from maptile2 import Mapset
import math


Tilelist = Mapset
MW, MH = 1024, 768

open_canvas(MW, MH)
map_bg = load_image('bg.jpg')
timg = load_image('block32_pr.png')
mimg = load_image('mario_t.png')
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
                chr.jump(10)
            if event.key == SDLK_a:
                chr.hit()
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
            timg.clip_draw(Tilelist[i].sptype*32, 0, 32, 32, Tilelist[i].hbleft + 16 - cmpPos, Tilelist[i].hbdown + 16)


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


    chr.draw(mimg, Tilelist)
    chr.xyrun(0,0)
    update_canvas()

    handle_events()
    delay(0.01)
close_canvas()
