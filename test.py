from robotlib import Robot, SerialArduino
import time

import threading

import math

robot = Robot()
dist = SerialArduino()
stop = 0

def add_angle(last, angle):
    
    myangle = last + angle
    
    while myangle < 0:
        myangle = 360 + myangle             # BWhile loop for many turn around

    return myangle



def calcul_pos(position, hypotenuse, angle):

    x = math.sin(math.radians(angle)) * hypotenuse
    y = math.cos(math.radians(angle)) * hypotenuse

#    if 90 < angle <= 180:
#        y = -y
#    elif 180 < angle <= 270:
#        x = -x
#        y = -y
#    elif 270 < angle <= 360:
#        x = -x

    return {'x': int(position['x'] + x), 'y': int(position['y'] + y)}


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
        self.position = {'x': 0, 'y': 0}
        distance = 0
        last_angle = 0 
        
        while stop == 0:
            robot.avance(1)
            distance += 1

            if dist.middle < 20 or dist.left < 20 or dist.right < 20:
                
                self.position = calcul_pos(self.position, distance, last_angle)
                
                if (dist.left < 25 and dist.right < 25):
                    robot.droite(60) # Mur
                    last_angle = add_angle(last_angle, 60)
                elif dist.left < 25 and dist.right > 25:
                        robot.droite(30) # Obstacle on left
                        last_angle = add_angle(last_angle, 30)
                elif dist.right < 25 and dist.left > 25:
                        robot.gauche(30)
                        last_angle = add_angle(last_angle, -30)
                elif dist.middle < 25:
                    if dist.right > dist.left:
                        robot.droite(60)
                        last_angle = add_angle(last_angle, 60)
                    else:
                        robot.gauche(60)
                        last_angle = add_angle(last_angle, -60)
                
                distance=0

        print(self.position)


try:
    arduino = Thread_Distance()
    bot = Thread_Avance()

    arduino.start()
    bot.start()

    bot.join()
    arduino.join()

except KeyboardInterrupt:
    stop=1
