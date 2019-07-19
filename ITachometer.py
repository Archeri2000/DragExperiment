import subprocess
import sys
import time

CONST_TACHO_DRIVER = 'uni-t-ut372:conn=1a86.e008'
SYSROK_CLI = ['D:\Program Files (x86)\sigrok\sigrok-cli\sigrok-cli', '-d', CONST_TACHO_DRIVER, '--continuous']


# Uses sysrok CLI to communicate with UT372
class Tachometer:

    # Initialises Tachometer with stdout callbacks
    def __init__(self, callback, addr=None):
        if addr is not None:
            SYSROK_CLI[0] = addr
        self.startTime = time.time()
        self.callback = callback
        pass

    # Begins monitoring Tachometer stdout
    def startMonitoring(self):
        try:
            print("Begin Monitoring")
            print(SYSROK_CLI)
            proc = subprocess.Popen(SYSROK_CLI, stdout=subprocess.PIPE)
            while proc.poll() is None:
                reading = proc.stdout.readline().decode('UTF-8')[4:-5]
                timestamp = time.time() - self.startTime
                self.callback(float(reading), timestamp)
        except:
            err = str(sys.exc_info()[1]) + "\n"
            output = err
            print(output + "error")
            exit()

    def setTiming(self):
        self.startTime = time.time()

