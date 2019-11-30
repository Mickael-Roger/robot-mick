from robotlib import Robot, SerialArduino
import time


robot = Robot()
dist = SerialArduino()

#for i in range(1,30):
#    robot.avance(1)
#    dist.readline()

dist.readline()
robot.avance(30)
for i in range(1,50):
    dist.readline()
    time.sleep(0.300)
