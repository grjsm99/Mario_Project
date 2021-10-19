from pico2d import *

class Frac:

    def __init__(self, x, y, xsp, ysp):
        self.x = x
        self.y = y
        self.xsp = xsp
        self.ysp = ysp
    def upd(self):
        self.x += self.xsp
        self.y += self.ysp
        self.ysp -= 0.3
    def rtxy(self):
        return self.x, self.y

