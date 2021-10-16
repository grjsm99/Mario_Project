from pico2d import *

class Frac:
    img = load_image('./img/frac.png')
    def __init__(self, x, y, xsp, ysp):
        self.x = x
        self.y = y
        self.xsp = xsp
        self.ysp = ysp
    def draw(self, cmpPos):
        self.x += self.xsp
        self.y += self.ysp
        self.ysp -= 0.3
        Frac.img.draw(self.x - cmpPos, self.y)

