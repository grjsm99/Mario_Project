from pico2d import *
from Gravity import *
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
        self.mushAni = 0
        self.isMushAni = False
        self.mushRate = 0
    def chuplook(self, value):  # 위아래 보는상태
        self.uplook = value

    def resetMotion(self):
        self.motion = 0
    def rtView(self):
        return self.camPos

    def setfric(self):
        self.fric = True

    def jump(self, power):
        self.isjump = True
        self.ysp = power

    def eat_Mushroom(self):
        self.isMushAni = True
        self.mushRate = 9
    def mush_Ani(self):
        if self.mode == 1:
            self.mode = 0
            self.width = 27
            self.height = 39
            delay(0.05)
        elif self.mode == 0:
            self.mode = 1
            self.width = 28
            self.height = 52
            delay(0.05)
        self.mushRate -= 1
        if self.mushRate == 0:
            self.isMushAni = False
    def xyrun(self, type, speed):
        if type==0: # x
            self.fric = False
            self.xsp = speed
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
            if self.ysp < 0 and (cleft < moblist[i].xpos + moblist[i].width) and (cright > moblist[i].xpos) and cdown < moblist[i].ypos + moblist[i].height and not cup < moblist[i].ypos + moblist[i].height: # 몹 밟음
                print(cdown, self.ysp, moblist[i].up, moblist[i].down)
                self.ysp = 8
                self.isjump = True
                print(cleft, cright, moblist[i].left, moblist[i].right)

                del moblist[i] 

    def motionUpdate(self, tileset):
        
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
        self.yacc-=0.03
        if self.ysp > -10:
            self.ysp += self.yacc   

        self.Collide(tileset)

        
        self.frame+=1
        if self.ysp > 0:
            self.motion = 2
        elif self.ysp < 0:
            self.motion = 3   
        elif self.xsp != 0 and self.ysp == 0 and self.frame%5==0: # 걷는모션
            if(self.motion == 0): self.motion = 1
            elif(self.motion == 1): self.motion = 0
            self.frame=0
        
        if self.ysp != 0:
            self.isjump = True
        if self.aning == False:
            if self.xpos + self.xsp > 0: self.xpos += self.xsp
            self.ypos += self.ysp
        self.chView()
        

        if self.isStop() == True:
            if self.uplook == 1:
                self.motion = 4
            if self.uplook == 2:
                self.motion = 5

    def draw(self):
        
        draw_rectangle(self.xpos - self.camPos, self.ypos , self.xpos + self.width- self.camPos , self.ypos + self.height)
        if self.flip == False:
            self.img.clip_draw(self.motion * self.width, 52-self.mode*52, self.width, self.height, self.xpos-self.camPos-self.mode+self.width/2, self.ypos+self.height/2)
        else:
            self.img.clip_composite_draw(self.motion * self.width, 52-self.mode*52, self.width, self.height, 0, 'h', self.xpos-self.camPos+self.width/2, self.ypos+self.height/2, self.width, self.height)


    def ColAct(self, type, t):
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
