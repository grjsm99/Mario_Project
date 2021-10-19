from pico2d import delay
running = None
temp = None

def run(state):
    global running
    running = True
    state.init()
    while(running):
        state.handle_events()
        state.update()
        state.draw()
        delay(0.01)
    

def quit():
    global running
    running = False