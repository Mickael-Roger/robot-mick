from robotlib import Robot
import time

import json

print("Robot is starting ... ", end = '')

robot = Robot()

print ("done. Press Ctrl C to stop the Robot")

try:
    while True:
        left, middle, right = robot.arduino.obstacle()
        print(left, middle, right)
        for elem in robot.camera.identify():
            print ("Found : ", elem["category"])

        time.sleep(3)

except KeyboardInterrupt:
    del robot


