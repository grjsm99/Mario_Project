import Framework
from pico2d import *
import start_state

MW, MH = 1024, 768

open_canvas(MW, MH)
Framework.run(start_state)
close_canvas()
    