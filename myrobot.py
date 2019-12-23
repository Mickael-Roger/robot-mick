from robotlib import Robot, SerialArduino
import time

import threading

robot = Robot()
dist = SerialArduino()
lock = threading.Lock()
stop = 0

class Thread_Distance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        global lock
        dist.obstacle()

class Thread_Avance(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dist
        global robot
        while stop == 0:
            robot.avance(1)
            if dist.middle < 20 or dist.left < 20 or dist.right < 20:
                if dist.right < 3:
                    robot.recule(5)
                    robot.gauche(90)
                elif dist.left < 3:
                    robot.recule(5)
                    robot.droite(90)
                elif (dist.left < 25 and dist.right < 25):
                    robot.droite(60) # Mur
                elif dist.left < 25 and dist.right > 25:
                        robot.droite(30) # Obstacle on left
                elif dist.right < 25 and dist.left > 25:
                        robot.gauche(30) # Obstacle on right


try:
    arduino = Thread_Distance()
    bot = Thread_Avance()

    arduino.start()
    time.sleep(0.1)
    bot.start()

    bot.join()
    arduino.join()

except KeyboardInterrupt:
    stop=1
