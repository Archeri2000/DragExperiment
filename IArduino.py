import serial, time


# Arduino controller class
class Arduino:
    # Intialises serial connection to Arduino through COM Port
    def __init__(self, COM_PORT):
        self.ardu = serial.Serial(COM_PORT, 9600, timeout=.1)
        time.sleep(1)

    # Polls current motor speed in 'COUNT'
    def pollSpeed(self):
        self.ardu.write('q\n'.encode('utf-8'))
        while not self.ardu.read() == b'a':
            pass
        return self.ardu.read_until('\n')

    # Increment motor speed by 'steps'
    def incSpeed(self, steps):
        for i in range(steps):
            self.ardu.write('m\n'.encode('utf-8'))

    # Decrement motor speed by 'steps'
    def decSpeed(self, steps):
        for i in range(steps):
            self.ardu.write('n\n'.encode('utf-8'))

    # Initialise experiment by lowering z-axis
    def initExperiment(self):
        self.ardu.write('i\n'.encode('utf-8'))

    # Ends experiment by raising z-axis
    def endExperiment(self):
        self.ardu.write('f\n'.encode('utf-8'))

    # Engage motor clutch and increase speed by 1
    def engageMotor(self):
        print("Engaging")
        self.ardu.write('e\n'.encode('utf-8'))


    # Disengage motor and decrease speed to 0
    def disengageMotor(self):
        print("Disengaging")
        self.ardu.write('d\n'.encode('utf-8'))

