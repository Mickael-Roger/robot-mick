from robotlib import Robot, SerialArduino
import time
import io
import json

import threading
from subprocess import Popen, PIPE

robot = Robot()
stop = 0

lock = threading.Lock()
PersonPosition = 0
PersonID = 0

class Thread_Tourne(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global PersonPosition
        global robot
        global stop
        global lock

        last_id = 0

        print("Start run")

        while stop == 0:
            lock.acquire()
            position = PersonPosition
            id = PersonID
            lock.release()

            if position != 0 and id != last_id:
                if position < 0.35:
                    robot.gauche(5)
                    print("gauche Pos ", position, " ID ", id, " Last ", last_id)
                elif position > 0.65:
                    robot.droite(5)
                    print("droite Pos ", position, " ID ", id, " Last ", last_id)
                else:
                    robot.avance(30)
                last_id = id

            time.sleep(0.5)

class Thread_identification(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        global PersonPosition
        global lock
        global PersonID

        with Popen(["./darknet", "detector", "demo", "coco.data", "yolov3-tiny.cfg", "yolov3-tiny.weights"], stdout=PIPE) as proc:
            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                response = json.loads(line)
                if response["category"] == "person":
                    objectsize = float(response["right"]) - float(response["left"])
                    objectmiddle = objectsize / 2.0
                    objectposition = objectmiddle + float(response["left"])

                    lock.acquire()
                    PersonPosition = objectposition
                    PersonID = PersonID+1
                    lock.release()

                    print(response)


try:

    bot = Thread_Tourne()
    darknet = Thread_identification()

    bot.start()
    darknet.start()

    bot.join()
    darknet.join()

except KeyboardInterrupt:
    stop=1
