from pico2d import *
from Gravity import *
import Framework
class Item(Gravity):
    def __init__(self, x, y, types):
        self.xpos = x * 32
        self.ypos = y * 32 - 32
        self.type = types # 0 = 동전, 1 = 버섯, 2 = 꽃, 3 = 라이프버섯
        self.motion = 0
        
        if self.type == 0:
            self.frame = 0

        if self.type == 1 or self.type == 3:
            self.xsp = -1
            self.ysp = 0
        if self.type == 5:
            self.ysp = 5
            self.xsp = 1
            self.yacc = 0
            self.type = 1
        self.height = 32
        self.width = 30
        self.left = self.xpos
        self.right = self.xpos + self.width
        self.down = self.ypos
        self.up = self.ypos + self.height
        self.camPos = 0


    def motionUpdate(self, tileset):
        if self.type == 0: # 동전
            self.frame += Framework.runtime
            if self.frame > 10:
                self.motion += 1
                self.motion %= 4
                self.frame = 0
        if self.type == 1 or self.type == 3: # 버섯
            if self.xsp < 0:
                self.flip = False
            if self.xsp > 0:
                self.flip = True
            self.yacc-=0.04 * Framework.runtime
            if self.ysp > -20:
                self.ysp += self.yacc * Framework.runtime 

            self.Collide(tileset)

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