from ITachometer import Tachometer
from IArduino import Arduino
from IPostProcess import PostProcess
import sys

# Constants
START_ACCEL = 10
RPM_TOLERANCE = 200
TIME_TOLERANCE = 3
MAX_RPM = 3000
START_RPM = 3000
STEADY_TIME = 10
FINAL_RPM = 300
PORT = "COM5"
OUT_FILE = "output.csv"
reading_list = []
ACCEL = "ACCEL"
DECEL = "DECEL"
CALIB = "CALIB"

varMap = {"START_ACCEL": START_ACCEL,
          "RPM_TOLERANCE": RPM_TOLERANCE,
          "TIME_TOLERANCE": TIME_TOLERANCE,
          "MAX_RPM": MAX_RPM,
          "START_RPM": START_RPM,
          "STEADY_TIME": STEADY_TIME,
          "FINAL_RPM": FINAL_RPM,
          "PORT": PORT,
          "OUT_FILE": OUT_FILE}

def configureVariable(name, value):



# Manages callbacks from tachometer
class CallbackManager:
    def __init__(self, mode, callback):
        self.mode = mode
        self.callbacks = {mode: callback}

    # Change callback mode
    def changeMode(self, mode):
        if mode in self.callbacks:
            self.mode = mode

    # Add extra callback
    def addCallback(self, mode, callback):
        self.callbacks[mode] = callback

    # Remove callback
    def removeCallback(self, mode):
        self.callbacks.pop(mode)

    # Calls a callback
    def callBack(self, message, timestamp):
        print("Calling", self.mode)
        self.callbacks[self.mode](message, timestamp)


# Accelerating phase
def accelCallback(rpm, timestamp):
    global reading_list
    # Exit condition - RPM reach max
    if rpm >= MAX_RPM:
        reading_list = []
        # Change to calibration mode
        cm.changeMode(CALIB)
    # Check tolerance
    reading_list.append((rpm, timestamp))
    if abs(rpm - reading_list[0][0]) < RPM_TOLERANCE:
        if timestamp - reading_list[0][1] > TIME_TOLERANCE:
            ardu.incSpeed(1)
            reading_list = []
    else:
        while abs(rpm - reading_list[0][0]) > RPM_TOLERANCE and len(reading_list) > 0:
            reading_list.pop(0)
    print(rpm, timestamp)


# Calibrating phase
def calibrateRPMCallback(rpm, timestamp):
    global reading_list
    reading_list.append((rpm, timestamp))
    # Exit condition - Steady RPM
    if timestamp - reading_list[0][1] > STEADY_TIME:
        # Change to deceleration mode
        reading_list = []
        tacho.setTiming()
        ardu.disengageMotor()
        cm.changeMode(DECEL)
    if abs(rpm - MAX_RPM) < RPM_TOLERANCE:
        pass
    elif rpm > MAX_RPM:
        reading_list.append((rpm, timestamp))
        if (timestamp - reading_list[0][1] > TIME_TOLERANCE) and reading_list[0][0] > MAX_RPM:
            ardu.decSpeed(1)
            reading_list = []
    else:
        reading_list.append((rpm, timestamp))
        if (timestamp - reading_list[0][1] > TIME_TOLERANCE) and reading_list[0][0] < MAX_RPM:
            ardu.incSpeed(1)
            reading_list = []
    print(rpm, timestamp)


# Decelerating phase
def decelCallback(message, timestamp):
    pass
    print(message, timestamp)
    if message > FINAL_RPM:
        post.record(message, timestamp)
    else:
        ardu.endExperiment()
        print("Completed Experiment")
        post.terminate()
        exit()
# Creates callback  manager and load phases
cm = CallbackManager(ACCEL, accelCallback)
cm.addCallback(CALIB, calibrateRPMCallback)
cm.addCallback(DECEL, decelCallback)
# Create tachometer and arduino

# TESTING
cm.changeMode(ACCEL)

tacho = Tachometer(cm.callBack)
ardu = None
post = None


def main():
    args = sys.argv[1:]
    f = open(args[0], "r")

    global ardu, post
    ardu = Arduino(PORT)
    post = PostProcess(OUT_FILE)
    ardu.initExperiment()
    ardu.engageMotor()
    ardu.incSpeed(10)
    # Start monitoring tachometer
    tacho.startMonitoring()


if __name__ == "__main__":
    main()
