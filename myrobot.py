from robotlib import Robot
import time

import json

print("Robot is starting ... ", end = '', flush=True)

robot = Robot()

print ("done. Press Ctrl C to stop the Robot", flush=True)

try:
    while True:
        left, middle, right = robot.arduino.obstacle()
        print(left, middle, right)
        for elem in robot.camera.identify():
            print ("Found : ", elem["category"])

        time.sleep(3)

except KeyboardInterrupt:
    del robot


