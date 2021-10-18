from Component import *

class Block(Component):
    def __init__(self, left, up, spt):
        self.x = left
        self.y = up
        self.hbleft = self.x * 32
        self.hbup = self.y * 32
        self.hbdown = self.hbup - 32
        self.hbright = self.hbleft + 32
        self.sptype = spt
        self.isAni = False
        self.frame = 0
        self.subframe = 0
        self.frrate = 0
        self.dl = False

        if spt == 0 or spt == 6 or spt == 7:
            self.ishbox = False
            self.island = True
        elif spt == 1:
            self.ishbox = False
            self.island = False
        else:
            self.ishbox = True
            self.island = True
        if spt == 2:
            self.isAni = True
            self.frrate = 6
        if spt == 3:
            self.frrate = 4
    
    def ani(self):
        if self.isAni == True:
            self.subframe += 1
            if self.subframe == 10:
                self.frame = (self.frame + 1) % self.frrate
                self.subframe = 0
