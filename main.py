from pico2d import *
from mario import Mario
from Mob import Mob
import Framework
import life_state

from frac import Frac
from Item import Item
import math
import copy


BLOCK_TYPES = 8
MOB_TYPES = 2
ITEM_TYPES = 4
MW, MH = 1024, 768

bimglist = None
mimglist = None
iimglist = None
Tilelist = None
map_bg = None
fimg = None
fbimg = None
camPos = None
backPos = None
fraclist = None
chr = None
isRight = None
isLeft = None
isLeftMove = None
Tilelist = None
Itemlist_ = None
Moblist_ = None
itmpdata = None
def init():
    if(Framework.selectStage == 0):
        from maptile1 import Mapset
        from maptile1 import Moblist
        from maptile1 import Itemlist
    if(Framework.selectStage == 1):
        from maptile2 import Mapset
        from maptile2 import Moblist
        from maptile2 import Itemlist
    print("Init")
    global mimglist
    global bimglist
    global map_bg
    global fimg
    global fbimg
    global fraclist
    global camPos
    global backPos
    global chr
    global isRight
    global isLeft
    global isLeftMove
    global Tilelist
    global Moblist_
    global Itemlist_
    global iimglist
    Tilelist = copy.deepcopy(Mapset)
    Moblist_ = copy.deepcopy(Moblist)
    Itemlist_ = copy.deepcopy(Itemlist)
    map_bg = load_image('./img/bg.jpg')
    fimg = load_image('./img/frac.png')
    fbimg = load_image('./img/fireball.png')
    bimglist = []
    fraclist = []
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

    chr = Mario()
    isRight = False
    isLeft = False
    isLeftMove = False


def exit():
    print("main exit")
    global mimglist
    global bimglist
    global map_bg
    global fimg
    global fraclist
    global camPos
    global backPos
    global chr
    global isRight
    global isLeft
    global isLeftMove
    global Tilelist
    global Moblist_
    global Itemlist_
    global fbimg

    del(mimglist)
    del(bimglist)
    del(map_bg)
    del(fimg)
    del(fraclist)
    del(camPos)
    del(chr)
    del(isRight)
    del(isLeft)
    del(isLeftMove)
    del(fbimg)
    Tilelist = None
    Moblist_ = None
    Itemlist_ = None

    

def handle_events():
    global running  
    global isRight
    global isLeft
    global isLeftMove
    global Moblist_
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
                chr.jump(8)
            if event.key == SDLK_a:
                #chr.eat_Mushroom()
                chr.launchFb()
                pass
            if event.key == SDLK_b:
                chr.rtxy()
                for i in range(len(Moblist_)):
                    Moblist_[i].rtxy()
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

    draw_mob()
    draw_item()
    draw_fb()
    chr.draw()

    update_canvas()
    chr.delayCheck()

def draw_mob():
    for i in range(len(Moblist_)):
        if Moblist_[i].xsp > 0:
            mimglist[Moblist_[i].type].clip_draw(Moblist_[i].motion * 32, 0, 32, Moblist_[i].height, Moblist_[i].xpos+16-camPos, Moblist_[i].ypos+Moblist_[i].height/2)
        elif Moblist_[i].xsp < 0:
            mimglist[Moblist_[i].type].clip_composite_draw(Moblist_[i].motion * 32, 0, 32, Moblist_[i].height, 0, 'h', Moblist_[i].xpos+16-camPos, Moblist_[i].ypos+Moblist_[i].height/2, Moblist_[i].width, Moblist_[i].height)
        #draw_rectangle(Moblist_[i].xpos - camPos, Moblist_[i].ypos, Moblist_[i].xpos - camPos + 32, Moblist_[i].ypos + Moblist_[i].height)

def draw_item():
    for i in range(len(Itemlist_)):
        iimglist[Itemlist_[i].type].clip_draw(Itemlist_[i].motion * 32, 0, 32, 32, Itemlist_[i].xpos+16-camPos, Itemlist_[i].ypos+Itemlist_[i].height/2)
        #draw_rectangle(Itemlist_[i].xpos - camPos, Itemlist_[i].ypos, Itemlist_[i].xpos - camPos + 32, Itemlist_[i].ypos + Itemlist_[i].height)


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

def draw_fb():
    global fbimg

    fblist = chr.drFb()
    for i in range(len(fblist)):
        fbimg.draw(fblist[i].xpos- camPos, fblist[i].ypos)


def update():
    if chr.dead_check() == True:
        Framework.chstate(life_state)
        return
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
    if chr.isMushAni == True:
        chr.mush_Ani()
    elif chr.isDeadAni == True:
        chr.dead_Ani()
    elif chr.isFireAni == True:
        chr.fire_Ani()
    else: 
        chr.motionUpdate(Tilelist)
        for i in range(len(Moblist_)):
            Moblist_[i].motionUpdate(Tilelist) # 몹 업데이트

        for i in range(len(Itemlist_)):
            Itemlist_[i].motionUpdate(Tilelist) # 아이템 업데이트

        for i in range(len(chr.firelist)):
            chr.firelist[i].motionUpdate(Tilelist) # 불 업데이트
            chr.firelist[i].CollideMob(Moblist_) # 불 몹충돌
            
        for i in range(len(chr.firelist)): 
            if(chr.firelist[i].dl == True):
                del(chr.firelist[i])
                return

        chr.CollideMob(Moblist_) # 몹충돌 검사
        result = chr.CollideItem(Itemlist_)  # 아이템 충돌 검사
        if(result==2): # 버섯 먹었을때
            chr.eat_Mushroom()
        if(result==3): # 꽃 먹었을때
            chr.eat_Flower()
        hitItem = chr.popItems()
        if(hitItem != None):
            if hitItem[2] == 0:
                Itemlist_.append(Item(hitItem[0], hitItem[1], 5)) # 튀어나오는 버섯
            else:
                Itemlist_.append(Item(hitItem[0], hitItem[1], 2)) # 꽃
            chr.itmpdata = None


         

    
#close_canvas()
