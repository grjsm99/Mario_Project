from pico2d import *
MW, MH = 1024, 768
class Gravity:
    xpos = 0
    ypos = 0
    width = 0
    height = 0
    yacc = 0

    def chView(self):
        if(self.xpos > MW // 2):
            self.camPos = self.xpos - MW // 2

    def Collide(self, tileset):
        chleft = self.xpos
        chright = self.xpos + self.width
        chup = self.ypos + self.height
        chdown = self.ypos
        type = None
        tl = None
        for i in range(len(tileset)):   # 충돌체크
            if tileset[i].island == True and ((chleft + self.xsp * 2 < tileset[i].hbright and chright + self.xsp * 2 > tileset[i].hbright) or (chright+ self.xsp * 2 > tileset[i].hbleft and chleft + self.xsp * 2 < tileset[i].hbleft) or (chright + self.xsp * 2 <= tileset[i].hbright and chleft + self.xsp * 2 >= tileset[i].hbleft)):
                if chup + self.ysp * 2 < tileset[i].hbdown or chdown + self.ysp * 2 > tileset[i].hbup:
                    pass
                else:
                    self.CollideCheck(tileset[i])
            if chright < tileset[i].hbleft: break

    def CollideCheck(self, t):
        chleft = self.xpos
        chright = self.xpos + self.width
        chup = self.ypos + self.height
        chdown = self.ypos
        draw_rectangle(t.hbleft - self.camPos, t.hbdown,t.hbleft - self.camPos + 32, t.hbdown + 32)
       
        if self.ysp <= 0 and chdown + self.ysp - t.hbup < 0 and chdown + self.ysp - t.hbup > self.ysp*2: # 착지판정
            if chleft < t.hbright and chright > t.hbleft:
                self.ColAct(0, t)
                return
        if t.ishbox == True:
            if self.ysp > 0 and chup - t.hbdown > 0 and chup - t.hbdown < 32: # 위로 부딪힐때 판정
                if chleft < t.hbright and chright > t.hbleft:
                    self.ColAct(1, t)  
                    return
            if (chup > t.hbdown and chdown < t.hbdown) or (chup > t.hbup and chdown < t.hbup) or (chup == t.hbup and chdown == t.hbdown): 
                if self.xsp >= 0 and chright + self.xsp - t.hbleft > 0 and chright + self.xsp - t.hbleft < 32: # 왼쪽벽 충돌
                    self.ColAct(2, t)
                    return
                if self.xsp <= 0 and chleft + self.xsp - t.hbright < 0 and chleft + self.xsp - t.hbright > -32: # 오른쪽벽 충돌
                    self.ColAct(3, t)
                    return


