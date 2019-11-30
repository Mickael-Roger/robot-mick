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

class Thread_Avance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        global robot
        try:
            while True:
                robot.avance(1)
                print("Middle ", dist.middle, " left ", dist.left, " right ", dist.right)
                if dist.middle < 30:
                    robot.recule(5)
                    robot.droite(90)
         except KeyboardInterrupt:
             robot.stop()


arduino = Thread_Distance()
bot = Thread_Avance()

arduino.start()
bot.start()

bot.join()
arduino.join()
