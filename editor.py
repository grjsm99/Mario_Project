from io import TextIOWrapper
from mario import Block
from maptile1 import Mapset
from pico2d import *
import re
MW, MH = 1024, 768
BLOCK_TYPES = 5
FILE_NAME = "maptile2.py"
Load_Tilelist = True  # False = 해당 파일이름으로 새파일 생성, True = 해당 파일이름의 파일 수정


open_canvas(MW, MH)
map_bg = load_image('bg.jpg')
timg = load_image('block32_pr.png')
mimg = load_image('mario_t.png')
camPos = 0
backPos = 0
Tilelist = list()
running = True
blockSelect = False
itemSelect = False
blockMode = 0
itemMode = 0
camMove = 0
dragMode = 0

if Load_Tilelist == True:
    fr = open(FILE_NAME , 'r')
    line = fr.readline()
    line = fr.readline()
    while line:
        line = fr.readline()
        if line[0] == ']':
            break
        vars = re.findall(r'\d+', line)
        print(vars[0],vars[1],vars[2])
        Tilelist.append(Block(int(vars[0]), int(vars[1]), int(vars[2])))
    fr.close()
def handle_events():
    global running
    global camPos
    global camMove
    global dragMode

    global itemMode
    global blockMode
    global itemSelect
    global blockSelect
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            if dragMode == 1:   # 생성
                addBlock((event.x + camPos) // 32, ((MH - event.y) // 32 + 1), blockMode)
            if dragMode == 2:
                checkExist((event.x + camPos) // 32, ((MH - event.y) // 32 + 1))
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if blockSelect == True:
                    print(event.x, event.y)
                    if event.y > 0 and event.y < 32 and event.x < 32 * BLOCK_TYPES:
                        blockMode = event.x // 32
                        blockSelect = False
                        return
                else:
                    addBlock((event.x + camPos) // 32, ((MH - event.y) // 32 + 1), blockMode)
                    dragMode = 1
            if event.button == SDL_BUTTON_RIGHT:
                 if blockSelect == False: dragMode = 2
        if event.type == SDL_MOUSEBUTTONUP:
            dragMode = 0
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                camMove = 1
            if event.key == SDLK_LEFT:
                camMove = 2           
            if event.key == SDLK_b:
                blockMode+=1
            if event.key == SDLK_1:
                blockSelect = True
            if event.key == SDLK_2:
                itemSelect = True
            
            if event.key == SDLK_s:
                Tilelist.sort(key=lambda c: c.x)
                f = open(FILE_NAME, 'w')
                f.write("from mario import Block\n")
                f.write("Mapset = [\n")
                for i in range(len(Tilelist)):
                    f.write("Block(%d, %d, %d),\n" % (Tilelist[i].hbleft // 32 , Tilelist[i].hbup // 32 , Tilelist[i].sptype))
                f.write("]\n")
                f.close()
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                camMove = 0
        if event.type == SDL_QUIT:
            running = False

def draw_tileset():
    global camPos
    global blockSelect
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - camPos >= 0 and Tilelist[i].hbleft - camPos <= MW:
            timg.clip_draw(Tilelist[i].sptype*32, 0, 32, 32, Tilelist[i].hbleft + 16 - camPos, Tilelist[i].hbdown + 16)
    if blockSelect == True:
        timg.draw_to_origin(0,MH-32)

def checkExist(x, y):
    global Tilelist
    for i in range(len(Tilelist)):
        x1 = Tilelist[i].hbleft // 32
        y1 = Tilelist[i].hbup // 32
        print((x1, y1), (x, y))
        if (x1, y1) == (x, y):
            Tilelist.remove(Tilelist[i])
            return

def addBlock(x, y, bMode):
    global Tilelist
    global blockMode
    global itemMode
    checkExist(x,y)
    Tilelist.append(Block(x, y, bMode))

while(running):
    if camMove == 1:
        camPos += 3
    elif camMove == 2:
        if camPos>=3:
            camPos -= 3
        else: camPos = 0
    clear_canvas()
    draw_tileset()
    update_canvas()
    handle_events()
    delay(0.01)
close_canvas()