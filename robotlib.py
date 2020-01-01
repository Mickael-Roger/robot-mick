import RPi.GPIO as GPIO
from time import sleep, time

import cv2 as cv
import sysv_ipc

import serial
import threading
from subprocess import Popen
import os
import sys

import json
import math

import smbus



lock = threading.Lock()
stop = 0


class Robot:

    # L298N to Raspberry GPIO ports
    in1 = 13
    in2 = 15
    ena = 11
    in3 = 24
    in4 = 26
    enb = 22

    # Acceleration / angle map
        # From 15 degrees to 360 degrees
    gyromap = (0, 135, 400, 750, 1075, 1450, 1850, 2150, 2550, 2900, 3250, 3675, 4100, 4375, 4700, 5150, 5550, 5850, 6200, 6600, 7050, 7400, 7700, 7950, 8500)

    def __del__(self):
        global stop

        if self.camera.cap.isOpened():
            self.darknet.kill()
            self.camera.reicvmq.send("", True, type=1)
            self.camera.sendmq.remove()
            self.camera.reicvmq.remove()
        
        stop = 1
        self.arduino.join()
        self.camera.join()
        GPIO.cleanup()


    def stop(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def __init__(self):

            # MPU6050 values
        PWR_MGMT_1   = 0x6B
        SMPLRT_DIV   = 0x19
        CONFIG       = 0x1A
        GYRO_CONFIG  = 0x1B
        INT_ENABLE   = 0x38


        self.Device_Address = 0x68


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

        self.position = {'x': 0.0, 'y': 0.0, 'angle': 0}

        # MPU6050 Init
        self.bus = smbus.SMBus(1)

        self.bus.write_byte_data(self.Device_Address, SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.Device_Address, PWR_MGMT_1, 1)
        self.bus.write_byte_data(self.Device_Address, CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.Device_Address, INT_ENABLE, 1)

        # Wait for MPU6050 stabilization
        sleep(3)

        # Arduino board
        self.arduino = self.Arduino()
        self.arduino.start()

        # Camera
        self.camera = self.Camera()
        self.camera.start()

        # Initialise darknet
        if self.camera.cap.isOpened():
            self.darknet = Popen(["./darknet-robot"])
            # Wait for darknet to start
            sleep(5)


    class Camera(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)

            # Start opencv Video camera
            self.cap = cv.VideoCapture(0)
            
            if self.cap.isOpened():
                
                self.capid = 0
                # Start message queue; Destroy it then recreate it
                self.sendmq = sysv_ipc.MessageQueue(2468, sysv_ipc.IPC_CREAT)
                self.reicvmq = sysv_ipc.MessageQueue(1357, sysv_ipc.IPC_CREAT)
                self.sendmq.remove()
                self.reicvmq.remove()
                self.sendmq = sysv_ipc.MessageQueue(2468, sysv_ipc.IPC_CREAT)
                self.reicvmq = sysv_ipc.MessageQueue(1357, sysv_ipc.IPC_CREAT)

                # Frame
                self.frame = None


        def run(self):
            global stop

            if self.cap.isOpened():
                while stop == 0:
                    ret, myframe = self.cap.read()
                    if ret:
                        self.frame = myframe
        

        def identify(self):
            results = []

            if self.cap.isOpened():
                cv.imwrite("/tmp/frame%d.jpg" % self.capid, self.frame)
                # Send request 
                msg_file = str(self.capid) + ";/tmp/frame" + str(self.capid) + ".jpg\0"
                self.sendmq.send(msg_file, True, type=1)

                # Wait for identification
                message = self.reicvmq.receive()

                os.remove("/tmp/frame" + str(self.capid) + ".jpg") 

                # Extract json from message
                
                jsonidx = message[0].find(b'\x00')
                if jsonidx == 0:
                    jsonmsg = ""
                else:
                    jsonmsg = message[0][:jsonidx].decode("utf-8")


                try:
                    for response in jsonmsg.split(';'):
                        result = json.loads(response)
                        results.append(result) 
                except:
                    pass

            return results



    def read_mpu6050_data(self, addr):
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)

        value = ((high << 8) | low)

        # MPU6050 use unsigned short int
        if(value > 32768):  
            value = value - 65536
        
        return abs(value)

    def wait_angle(self, angle):

        mpuregister = 0x47

        while angle > 0:
            
            if angle > 360:
                myangle = 360
            else:
                myangle = angle
            
            # Define the MPU6050 G values
            if myangle % 15:
                i, d = divmod(myangle/15, 1)
                index = int(i)
                mpuvalue = (self.gyromap[index] + self.gyromap[index+1]) / 2
            else:
                mpuvalue = self.gyromap[int(myangle/15)]
            
            valgz = 0

            while valgz < mpuvalue:

                deb = time()
                gyro_z = self.read_mpu6050_data(mpuregister)
                valgz += gyro_z/131.0
                
                # Must read 1 value per 5 ms
                wait = 0.005 - (time() - deb)
                if wait > 0:
                    sleep(wait)

            angle -= 360

    def print_position(self):
        print(self.position)

    def add_angle(self, angle):
        self.position['angle'] = self.position['angle'] + angle

        while self.position['angle'] < 0:
            self.position['angle'] = 360 + self.position['angle']           # BWhile loop for many turn around
        
        while self.position['angle'] > 360:
            self.position['angle'] = self.position['angle'] - 360           # While loop for many turn around on right   
    
    def home(self):
        self.stop()
        sleep(1)

        rotation = math.degrees(math.atan2(abs(self.position['y']), abs(self.position['x'])))
        distance = abs(self.position['x']) / math.cos(math.radians(rotation))

        # Calculate direction
        if self.position['x'] >= 0 and self.position['y'] >= 0:
            direction = 270 - rotation

        elif self.position['x'] >= 0 and self.position['y'] < 0:
            direction = 270 + rotation

        elif self.position['x'] < 0 and self.position['y'] < 0:
            direction = 90 - rotation

        elif self.position['x'] < 0 and self.position['y'] >= 0:
            direction = 90 + rotation


        # Left move to the direction
        if self.position['angle'] <= direction:
            left_dist = self.position['angle'] + (360 - direction)
        else:
            left_dist = self.position['angle'] - direction

    
        if left_dist > 180:
            self.droite(360 - left_dist)
        else:
            self.gauche(left_dist)
        
        self.avance(distance)

    def avance(self, nb):
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        sleep(0.1 * nb)
        self.stop()
        self.calcul_pos(nb)

    def recule(self, nb):

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        sleep(0.1 * nb)
        self.stop()
        ############ self.calcul_pos(nb) # TODO
        
    def droite(self, nb):
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)

        self.wait_angle(nb)
        self.stop()
        self.add_angle(nb)

    def gauche(self, nb):
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        
        self.wait_angle(nb)
        self.stop()
        self.add_angle(-nb)


    def calcul_pos(self, distance):
        
        x = math.sin(math.radians(self.position['angle'])) * distance
        y = math.cos(math.radians(self.position['angle'])) * distance

        self.position['x'] = self.position['x'] + x
        self.position['y'] = self.position['y'] + y


    class Arduino(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)
            self.middle = 99
            self.left = 99
            self.right = 99

            self.ser.reset_input_buffer()

        def obstacle(self):
            lock.acquire()
            left = self.left
            middle = self.middle
            right = self.right
            lock.release()

            return left, middle, right

        def run(self):
            global lock
            global stop

            while stop == 0:
                msg = str(self.ser.readline().decode("utf-8")).rstrip()
                try:
                    response = json.loads(msg)
                    lock.acquire()
                    self.middle = int(response["middle"]) - 3
                    self.left = int(response["left"])
                    self.right = int (response["right"])
                    lock.release()
                except:
                    pass
                
                sleep(0.05)    

