from pico2d import *

MW, MH = 1024, 768

class Mario:
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

    def chView(self):
        if(self.xpos > MW // 2):
            self.camPos = self.xpos - MW // 2

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
        self.mode = 1
        self.width = 28
        self.height = 52

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

    
    def CollideCheck(self, t):
        chleft = self.xpos
        chright = self.xpos + self.width
        chup = self.ypos + self.height
        chdown = self.ypos
        draw_rectangle(t.hbleft - self.camPos, t.hbdown,t.hbleft - self.camPos + 32, t.hbdown + 32)

       
        if self.ysp <= 0 and chdown + self.ysp - t.hbup < 0 and chdown + self.ysp - t.hbup > self.ysp*2: # 착지판정
            if chleft < t.hbright and chright > t.hbleft:
                if(self.ypos!=t.hbup): self.motion = 0
                self.ypos = t.hbup
                self.yacc = 0
                self.ysp = 0
                self.isjump = False
            return

        if t.ishbox == True:
            if self.ysp > 0 and chup - t.hbdown > 0 and chup - t.hbdown < 32: # 위로 부딪힐때 판정
                if chleft < t.hbright and chright > t.hbleft:
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
                    return
            if (chup > t.hbdown and chdown < t.hbdown) or (chup > t.hbup and chdown < t.hbup): 
                if self.xsp >= 0 and chright + self.xsp - t.hbleft > 0 and chright + self.xsp - t.hbleft < 32: # 왼쪽벽 충돌
                    self.xpos = t.hbleft - self.width
                    self.xsp = 0
                    return 
                if self.xsp <= 0 and chleft + self.xsp - t.hbright < 0 and chleft + self.xsp - t.hbright > -32: # 오른쪽벽 충돌
                    self.xpos = t.hbright
                    self.xsp = 0
                    return



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

        chleft = self.xpos
        chright = self.xpos + self.width
        chup = self.ypos + self.height
        chdown = self.ypos
        for i in range(len(tileset)):   # 충돌체크
            if tileset[i].island == True and ((chleft + self.xsp * 2 < tileset[i].hbright and chright + self.xsp * 2 > tileset[i].hbright) or (chright+ self.xsp * 2 > tileset[i].hbleft and chleft + self.xsp * 2 < tileset[i].hbleft) or (chright + self.xsp * 2 <= tileset[i].hbright and chleft + self.xsp * 2 >= tileset[i].hbleft)):
                if chup + self.ysp * 2 < tileset[i].hbdown or chdown + self.ysp * 2 > tileset[i].hbup:
                    pass
                else:
                    self.CollideCheck(tileset[i])  
            if chright < tileset[i].hbleft: break

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

    def draw(self, t):
        self.motionUpdate(t)
        draw_rectangle(self.xpos - self.camPos, self.ypos , self.xpos + self.width- self.camPos , self.ypos + self.height)
        if self.flip == False:
            self.img.clip_draw(self.motion * self.width, 52-self.mode*52, self.width, self.height, self.xpos-self.camPos-self.mode+self.width/2, self.ypos+self.height/2)
        else:
            self.img.clip_composite_draw(self.motion * self.width, 52-self.mode*52, self.width, self.height, 0, 'h', self.xpos-self.camPos+self.width/2, self.ypos+self.height/2, self.width, self.height)
