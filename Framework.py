from pico2d import delay
running = None
temp = None
runningState = None
selectStage = 1
life = 9
def run(state = None):
    global runningState
    global running
    running = True
    runningState = state
    runningState.init()
    while(running):
        runningState.handle_events()
        runningState.update()
        runningState.draw()
        delay(0.01)
    
def chstate(tar):
    global running
    global runningState
    print(runningState , " - > " , tar , " , ")

    runningState.exit()
    runningState = tar
    tar.init()




def quit():
    global running
    global runningState
    running = False
    runningState = None
