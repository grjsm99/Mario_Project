from io import TextIOWrapper
from Block import Block
from pico2d import *
from Mob import Mob
from Item import Item
import re
MW, MH = 1024, 768
BLOCK_TYPES = 8
MOB_TYPES = 2
ITEM_TYPES = 0
FILE_NAME = "maptile2.py"
Load_Tilelist = True  # False = 해당 파일이름으로 새파일 생성, True = 해당 파일이름의 파일 수정


open_canvas(MW, MH)
map_bg = load_image('./img/bg.jpg')
timg = load_image('./img/block32_pr.png')
mimg = load_image('./img/mob32.png')
bimglist = []
mimglist = []
iimglist = []
for i in range(BLOCK_TYPES):
    bimglist.append(load_image("./img/b%d.png" % i))
for i in range(MOB_TYPES):
    mimglist.append(load_image("./img/m%d.png" % i))
for i in range(ITEM_TYPES):
    iimglist.append(load_image("./img/i%d.png" % i))
camPos = 0
backPos = 0
Moblist = list()
Tilelist = list()
Itemlist = list()
running = True
Selectmode = 0 # 0 = 블럭, 1 = 몹, 2 = 아이템
blockSelect = False
MobSelect = False
ItemSelect = False
num = 0
camMove = 0
dragMode = 0

if Load_Tilelist == True:
    fr = open(FILE_NAME , 'r')
    line = fr.readline()
    line = fr.readline()
    line = fr.readline()
    line = fr.readline()
    mode = 0
    while line:
        line = fr.readline()
        if line[0] == ']':
            mode += 1
            line = fr.readline()
            line = fr.readline()
        vars = re.findall(r'\d+', line)
        if mode == 0: Tilelist.append(Block(int(vars[0]), int(vars[1]), int(vars[2])))
        if mode == 1: Moblist.append(Mob(int(vars[0]), int(vars[1]), int(vars[2])))
def handle_events():
    global running
    global camPos
    global camMove
    global dragMode
    global Selectmode
    global ItemSelect
    global MobSelect
    global blockSelect
    global num
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            if dragMode == 1:   # 생성
                addBlock((event.x + camPos) // 32, ((MH - event.y) // 32 + 1), num, Selectmode)
            if dragMode == 2:
                checkExist((event.x + camPos) // 32, ((MH - event.y) // 32 + 1), Selectmode)
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if blockSelect == True:
                    #print(event.x, event.y)
                    if event.y > 0 and event.y < 32 and event.x < 32 * BLOCK_TYPES:
                        num = event.x // 32
                        blockSelect = False
                        Selectmode = 0
                        return
                elif MobSelect == True:
                    if event.y > 0 and event.y < 50 and event.x < 32 * MOB_TYPES:
                        num = event.x // 32
                        MobSelect = False
                        Selectmode = 1
                        return
                elif ItemSelect == True:
                    if event.y > 0 and event.y < 50 and event.x < 32 * ITEM_TYPES:
                        num = event.x // 32
                        ItemSelect = False
                        Selectmode = 2
                        return
                else:
                    addBlock((event.x + camPos) // 32, ((MH - event.y) // 32 + 1), num, Selectmode)
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
            if event.key == SDLK_1:
                blockSelect = True
                MobSelect = False
                ItemSelect = False
            if event.key == SDLK_2:
                MobSelect = True
                blockSelect = False
                ItemSelect = False
            if event.key == SDLK_3:
                ItemSelect = True
                blockSelect = False
                MobSelect = False
            if event.key == SDLK_s:
                Tilelist.sort(key=lambda c: c.x)
                f = open(FILE_NAME, 'w')
                f.write("from Block import Block\n")
                f.write("from Mob import Mob\n")
                f.write("from Item import Item\n")
                f.write("Mapset = [\n")
                for i in range(len(Tilelist)):
                    f.write("Block(%d, %d, %d),\n" % (Tilelist[i].hbleft // 32 , Tilelist[i].hbup // 32 , Tilelist[i].sptype))
                f.write("]\n")
                f.write("Moblist = [\n")
                for i in range(len(Moblist)):
                    f.write("Mob(%d, %d, %d),\n" % (Moblist[i].left // 32 , Moblist[i].up // 32 - 1, Moblist[i].type))
                f.write("]\n")
                f.close()
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                camMove = 0
        if event.type == SDL_QUIT:
            running = False

def draw_tileset(typ):
    global camPos
    for i in range(len(Tilelist)):
        if Tilelist[i].hbright - camPos >= 0 and Tilelist[i].hbleft - camPos <= MW:
            bimglist[Tilelist[i].sptype].clip_draw(Tilelist[i].frame * 32, 0, 32, 32, Tilelist[i].hbleft + 16 - camPos, Tilelist[i].hbdown + 16)
    for i in range(len(Moblist)):
        if Moblist[i].right - camPos >= 0 and Moblist[i].left - camPos <= MW:
            mimglist[Moblist[i].type].clip_draw(Moblist[i].frame * 32, 0, 32, Moblist[i].height, Moblist[i].xpos + 16 - camPos, Moblist[i].ypos - 16)
    if blockSelect == True:
        timg.draw_to_origin(0, MH - 32)
    if MobSelect == True:
        mimg.draw_to_origin(0, MH - 50)

def checkExist(x, y, type):
    global Tilelist
    global Moblist
    global Itemlist
    if type == 0:
        for i in range(len(Tilelist)):
            x1 = Tilelist[i].hbleft // 32
            y1 = Tilelist[i].hbup // 32
            if (x1, y1) == (x, y):
                Tilelist.remove(Tilelist[i])
                return
    if type == 1:
        for i in range(len(Moblist)):
            x1 = Moblist[i].xpos // 32
            y1 = Moblist[i].ypos // 32
            if (x1, y1) == (x, y):
                Moblist.remove(Moblist[i])
                return
    if type == 2:
        for i in range(len(Itemlist)):
            x1 = Itemlist[i].xpos // 32
            y1 = Itemlist[i].ypos // 32
            if (x1, y1) == (x, y):
                Itemlist.remove(Itemlist[i])
                return

def addBlock(x, y, bMode, type): # 0 = 블럭, 1 = 몹, 2 = 아이템
    global Tilelist
    global blockMode
    global itemMode
    checkExist(x,y, type)
    if(type == 0): Tilelist.append(Block(x, y, bMode))
    if(type == 1): Moblist.append(Mob(x, y, bMode))
    if(type == 2): Itemlist.append(Block(x, y, bMode))

while(running):
    if camMove == 1:
        camPos += 6
    elif camMove == 2:
        if camPos>=6:
            camPos -= 6
        else: camPos = 0
    clear_canvas()
    draw_tileset(Selectmode)
    update_canvas()
    handle_events()
    delay(0.01)
close_canvas()