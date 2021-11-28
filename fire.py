from pico2d import *
from Gravity import *

class Fire(Gravity):
    def __init__(self, x, y, isr):
        self.xpos = x + 14
        self.ypos = y + 26
        self.ysp = 2
        self.yacc = 0
        self.height = 16
        self.width = 16
        self.camPos = 0
        self.timer = 200
        self.dl = False
        if(isr == True):
            self.xsp = 2
        else:
            self.xsp = -2
    def CollideMob(self, moblist):
        cleft = self.xpos + self.xsp
        cright = self.xpos + self.width + self.xsp
        cdown = self.ypos
        cup = self.ypos + self.height
        for i in range(len(moblist)):
            if (cleft < moblist[i].xpos + moblist[i].width) and (cright > moblist[i].xpos) and (cdown < moblist[i].ypos + moblist[i].height) and (cup > moblist[i].ypos):
                    del moblist[i]
                    self.dl = True
                    return 0


    def motionUpdate(self, tileset):
        self.timer -= 1 * Framework.runtime
        self.yacc -= 0.04 * Framework.runtime
        if self.ysp > -20:
            self.ysp += self.yacc * Framework.runtime

        self.Collide(tileset)

        self.xpos += self.xsp * Framework.runtime
        self.ypos += self.ysp * Framework.runtime
        if(self.timer<0):
            self.dl = True
        
    def ColAct(self, type, t):
        if type == 0: # 착지
            self.ypos = t.hbup
            self.yacc = 0
            self.ysp = 3
        elif type == 2: # 왼쪽
            self.xpos = t.hbleft - self.width
            self.xsp *= -1
        elif type == 3: # 오른쪽
            self.xpos = t.hbright
            self.xsp *= -1