from pico2d import *
from Gravity import *
from fire import Fire
import Framework
MW, MH = 1024, 768


class Mario(Gravity):
    def __init__(self):
        self.img = load_image('./img/mario_t.png')
        self.frame = 0
        self.mode = 0
        self.motion = 0
        self.fric = False
        self.flip = False
        self.width=27
        self.height=39
        self.xpos = 50 # Z마리오의 왼쪽끝
        self.ypos = 385 # 마리오의 아래끝
        self.xsp = 0
        self.ysp = 0
        self.yacc = 0
        self.isjump = False
        self.camPos = 0
        self.uplook = 0
        self.aning = False
        self.firelist = []
        self.isMushAni = False
        self.isFireAni = False
        self.mushRate = 0
        self.fireRate = 0
        self.frrate = 0

        self.isDeadAni = False
        self.deadDelay = False
        self.isdead = False
        self.inviscount = 0
        self.itmpdata = None

    def chuplook(self, value):  # 위아래 보는상태
        self.uplook = value

    def mobHit(self):
        if(self.mode == 2): # 불쏘는 상태일때
            self.isFireAni = True
            self.fireRate = 0
            self.inviscount = 1000
        elif(self.mode == 1):
            self.isMushAni = True
            self.mushRate = 0
            self.inviscount = 1000
        else:
            self.motion = 6

            self.ysp = 8 * Framework.runtime
            self.yacc = -0.16 * (Framework.runtime ** 2)
            self.isDeadAni = True
        
    def launchFb(self):
        if(self.mode == 2):
            self.firelist.append(Fire(self.xpos, self.ypos, self.flip))
    
    def drFb(self):
        return self.firelist

    def resetMotion(self):
        self.motion = 0
    def rtView(self):
        return self.camPos

    def setfric(self):
        self.fric = True

    def jump(self, power):
        self.isjump = True
        self.ysp = power

    def eat_Item(self, type):
        global life
        print(type)
        if(type == 2): # 버섯
            if self.mode == 0:
                self.isMushAni = True
                self.mushRate = 0
        if(type == 3): # 꽃
                self.isFireAni = True
                self.fireRate = 0
        if(type == 4): # 1UP
            Framework.life+=1
        if(type == 1): # 동전
            pass

            
    def mush_Ani(self):
        print(self.mushRate, Framework.runtime)
        if self.mushRate > 5:
            if self.mode == 1:
                self.mode = 0
                self.width = 27
                self.height = 39
        
            elif self.mode == 0:
                self.mode = 1
                self.width = 28
                self.height = 52
            self.mushRate = 0
            self.frrate += 1
        self.mushRate += Framework.runtime
        if self.frrate == 9:
            self.isMushAni = False
            self.frrate = 0

    def fire_Ani(self):
        if self.fireRate > 5:
            if self.mode == 2:
                self.mode = 1
            else:
                self.mode = 2
            self.fireRate = 0
            self.frrate += 1
        self.fireRate += Framework.runtime
        if self.frrate == 9:
            self.isFireAni = False
            self.frrate = 0

    def delayCheck(self):
        if self.deadDelay == False and self.isDeadAni == True:
            self.deadDelay = True
            delay(0.7)

    def dead_Ani(self):
        if self.yacc > 0.05:
            self.yacc = 0.05
        self.ypos += self.ysp 
        self.ysp += self.yacc
        if self.ypos < 0:
            self.isdead = True
        
    def dead_check(self):
        return self.isdead

    def xyrun(self, type, speed):
        if type==0: # x
            self.fric = False
            self.xsp = speed# * RUN_SPEED_PPS
        if type==1: # y
            self.ysp = speed

        
    def isNear(self, t):
        return True

    def isStop(self):
        if self.xsp == 0 and self.ysp == 0:
           return True
        else: False
    
    def hit(self):
        self.mode = 0

    def CollideMob(self, moblist):
        cleft = self.xpos + self.xsp
        cright = self.xpos + self.width + self.xsp
        cdown = self.ypos
        cup = self.ypos + self.height
        for i in range(len(moblist)):
            if (cleft < moblist[i].xpos + moblist[i].width) and (cright > moblist[i].xpos) and (cdown < moblist[i].ypos + moblist[i].height):
                if self.ysp < 0 and cdown - moblist[i].ypos - moblist[i].height > self.ysp and not cup < moblist[i].ypos + moblist[i].height: # 몹 밟음
                    self.yacc = 0
                    self.jump(6)
                    self.inviscount = 200
                    del moblist[i]
                    return 0
                elif cup > moblist[i].ypos and (self.inviscount == 0):
                    self.yacc = 0
                    self.mobHit() # 몹에 닿음
                    return 1
    def CollideItem(self, Itemlist):
        cleft = self.xpos + self.xsp
        cright = self.xpos + self.width + self.xsp
        cdown = self.ypos
        cup = self.ypos + self.height

        for i in range(len(Itemlist)):
            if (cleft < Itemlist[i].xpos + Itemlist[i].width) and (cright > Itemlist[i].xpos) and (cdown < Itemlist[i].ypos + Itemlist[i].height) and (cup > Itemlist[i].ypos):
                tmp = Itemlist[i].type
                del Itemlist[i]
                return tmp + 1
        return 0

    def motionUpdate(self, tileset):
        if self.ypos < 0:
            self.isdead = True
        if self.inviscount > 0:
            self.inviscount -= 1000 * Framework.frame_time # 무적시간 카운트 줄임
        if self.inviscount < 0:
            self.inviscount = 0
        if(self.inviscount == 0):
            self.img.opacify(1) # 무적시간 아닐때 선명하게 보이기

        else:   
            if self.inviscount % 2 == 0:
                self.img.opacify(20) # 몹 닿았을때 흐릿하게 보이기
            else:
                self.img.opacify(120) # 몹 닿았을때 흐릿하게 보이기

        if self.fric == True:   # x방향 멈출시 마찰력
            self.xsp *= 0.8
            if (self.xsp < 0.1 and self.xsp > 0) or (self.xsp > -0.1 and self.xsp < 0):
                self.xsp = 0
                self.fric = False

        if self.xsp == 0 and self.ysp == 0:
            self.motion = 0

        if self.xsp < 0:
            self.flip = False
        if self.xsp > 0:
            self.flip = True
        self.yacc-=0.04 * Framework.runtime
        if self.ysp > -20:
            self.ysp += self.yacc * Framework.runtime

        self.Collide(tileset)

        
        self.frame += Framework.runtime
        if self.ysp > 0:
            self.motion = 2
        elif self.ysp < 0:
            self.motion = 3   
        elif self.xsp != 0 and self.ysp == 0 and self.frame > 5: # 걷는모션
            if(self.motion == 0): self.motion = 1
            elif(self.motion == 1): self.motion = 0
            self.frame=0
        
        if self.ysp != 0:
            self.isjump = True
        if self.aning == False:
            if self.xpos + self.xsp > 0: self.xpos += self.xsp * Framework.runtime
            self.ypos += self.ysp * Framework.runtime
        self.chView()

        if self.isStop() == True:
            if self.uplook == 1:
                self.motion = 4
            if self.uplook == 2:
                self.motion = 5

    def draw(self):
        #draw_rectangle(self.xpos - self.camPos, self.ypos , self.xpos + self.width- self.camPos , self.ypos + self.height)
        if self.flip == False:
            self.img.clip_draw(self.motion * self.width, 104-self.mode*52, self.width, self.height, self.xpos-self.camPos-self.mode+self.width/2, self.ypos+self.height/2)
        else:
            self.img.clip_composite_draw(self.motion * self.width, 104-self.mode*52, self.width, self.height, 0, 'h', self.xpos-self.camPos+self.width/2, self.ypos+self.height/2, self.width, self.height)

    def popItems(self):
        return self.itmpdata

    def ColAct(self, type, t):
        print(type)
        if type == 0: # 착지
            if(self.ypos!=t.hbup): self.motion = 0
            self.ypos = t.hbup
            self.yacc = 0
            self.ysp = 0
            self.isjump = False

        elif type == 1: # 위 부딪힘
            self.ypos = t.hbdown - self.height
            self.yacc = 0
            self.ysp *= 0
            if t.sptype == 2: # 아이템 블록 부딪힘
                t.sptype = 4
                t.isAni = False
                t.frame = 0
                self.itmpdata = (t.x, t.y + 1, self.mode)
            if t.sptype == 3: # 돌아가는 블록 부딪힘
                t.isAni = True
                t.ishbox = False
                t.island = False
            if t.sptype == 5:
                t.dl = True       
        elif type == 2: # 왼쪽
            self.xpos = t.hbleft - self.width
            self.xsp = 0
        elif type == 3: # 오른쪽
            self.xpos = t.hbright
            self.xsp = 0
