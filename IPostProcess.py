import numpy
import pandas
from matplotlib import pyplot as plt
import subprocess
import sys
import os

CMD = "PostProcessor.py"


class PostProcess:
    def __init__(self, filename):
        self.proc = subprocess.Popen([sys.executable, CMD, os.getcwd()+"\\"+filename], stdin=subprocess.PIPE)
        self.proc.stdin.write(b"RPM, TIME")

    def record(self, val, time):
        try:
            print(val, time)
            self.proc.stdin.write(bytes("\n"+str(val)+", "+str(time), 'utf-8'))
        except:
            err = str(sys.exc_info()[1]) + "\n"
            output = err
            print(output + "error")
            exit()

    def terminate(self):
        try:
            self.proc.stdin.write(b"\nexit\n")
            print("Terminated")
        except:
            err = str(sys.exc_info()[1]) + "\n"
            output = err
            print(output + "error")
            exit()

