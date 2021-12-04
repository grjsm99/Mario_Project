from pico2d import delay
import time

frame_time = 0.0
runtime = 0.0
running = None
temp = None
runningState = None
selectStage = 1
life = 2
score = 0


PIXEL_PER_METER = 32.0
RUN_SPEED_KMPH = 8.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


def run(state = None):
    global runningState
    global running
    global frame_time
    global runtime

    running = True
    runningState = state
    runningState.init()
    current_time = time.time()
    while(running):
        runningState.handle_events()
        runningState.update()
        runningState.draw()
        #delay(0.01)
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time
        if(frame_time>0.03): frame_time = 0.03
        runtime = frame_time * RUN_SPEED_PPS
        #print("Frame Time: %f sec, Frame Rate: %f fps" %(frame_time,frame_rate))

    
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
