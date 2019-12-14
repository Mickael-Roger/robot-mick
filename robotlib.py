import RPi.GPIO as GPIO
from time import sleep, time

import serial
import sys

import json



class Robot:

    # L298N to Raspberry GPIO ports
    in1 = 13
    in2 = 15
    ena = 11
    in3 = 24
    in4 = 26
    enb = 22

    def __del__(self):
        GPIO.cleanup()


    def stop(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.ena,GPIO.OUT)
        GPIO.setup(self.enb,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

        self.p=GPIO.PWM(self.ena,1000)
        self.q=GPIO.PWM(self.enb,1000)
        self.p.start(100)
        self.q.start(100)

        self.p.ChangeDutyCycle(100)
        self.q.ChangeDutyCycle(100)
    
    
    def avance(self, nb):
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(0.1 * nb)
        self.stop()

    def recule(self, nb):

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        sleep(0.1 * nb)
        self.stop()
        
    def droite(self, nb):
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(0.0085 * nb)
        self.stop()

    def gauche(self, nb):
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        sleep(0.0085 * nb)
        self.stop()    


class SerialArduino:

    def __init__(self):
#        self.pattern = re.compile("\d+;\d+;\d+")
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)
        self.middle = 0
        self.left = 0
        self.right = 0

    def obstacle(self):

        self.ser.reset_input_buffer()

        while True:
            msg = str(self.ser.readline().decode("utf-8")).rstrip()
            try:
                response = json.loads(msg)
                self.middle = int(response["middle"]) - 3
                self.left = int(response["left"])
                self.right = int (response["right"])
            except:
                print("Error", sys.exc_info()[0])
                pass
            
                

