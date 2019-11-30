from robotlib import Robot, SerialArduino
import time

import threading

robot = Robot()
dist = SerialArduino()

class Thread_Distance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        dist.obstacle()


arduino = Thread_Distance()
arduino.start()

arduino.join()

for i in range(1,50):
    robot.avance(1)
    print("Middle ", dist.middle, " left ", dist.left, " right ", dist.right)
