from pico2d import *
from Gravity import *
import Framework
class Mob(Gravity):
    def __init__(self, x, y, types):
        self.frame = 0
        self.type = types
        self.width = 32
        self.height = 32
        if self.type == 1 : self.height += 18
        self.xpos = x * 32
        self.ypos = y * 32 - 32

        self.left = self.xpos
        self.right = self.xpos + self.width
        self.down = self.ypos
        self.up = self.ypos + self.height

        self.xsp = -1
        self.ysp = 0
        self.yacc = 0
        self.flip = False
        self.camPos = 0
        self.motion = 0
    
    def motionUpdate(self, tileset):
        if self.xsp < 0:
            self.flip = False
        if self.xsp > 0:
            self.flip = True
        self.yacc-=0.04 * Framework.runtime
        if self.ysp > -20:
            self.ysp += self.yacc * Framework.runtime

        self.Collide(tileset)
        self.frame+=Framework.runtime
        if self.xsp != 0 and self.ysp == 0 and self.frame > 5: # 걷는모션
            if(self.motion == 0): self.motion = 1
            elif(self.motion == 1): self.motion = 0
            self.frame=0
        self.xpos += self.xsp * Framework.runtime
        self.ypos += self.ysp * Framework.runtime
        
    def ColAct(self, type, t):
        if type == 0: # 착지
            self.ypos = t.hbup
            self.yacc = 0
            self.ysp = 0
        elif type == 2: # 왼쪽
            self.xpos = t.hbleft - self.width
            self.xsp *= -1
        elif type == 3: # 오른쪽
            self.xpos = t.hbright
            self.xsp *= -1
