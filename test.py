from robotlib import Robot, SerialArduino
import time

import threading

robot = Robot()
dist = SerialArduino()
stop = 0

class Thread_Distance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        dist.obstacle()

class Thread_Avance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        global robot
        while stop == 0:
            robot.avance(1)
            print("Middle ", dist.middle, " left ", dist.left, " right ", dist.right)
            if dist.middle < 20 or dist.left < 20 or dist.right < 20:
                robot.recule(2)
                robot.droite(90)


try:
    arduino = Thread_Distance()
    bot = Thread_Avance()

    arduino.start()
    bot.start()

    bot.join()
    arduino.join()

except KeyboardInterrupt:
    stop=1
