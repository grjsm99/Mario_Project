from pico2d import delay
running = None
temp = None
runningState = None
def run(state):
    global runningState
    global running
    running = True
    runningState = state
    state.init()
    while(running):
        state.handle_events()
        state.update()
        state.draw()
        delay(0.01)
    
def chstate(tar):
    global running
    global runningState

    runningState.exit()
    if runningState != None:
        runningState.init()



def quit():
    global running
    global runningState
    running = False
    runningState = None
