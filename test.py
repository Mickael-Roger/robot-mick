import RPi.GPIO as GPIO
from time import sleep, time


in1 = 10
in2 = 12
ena = 8

in3 = 24
in4 = 26
enb = 22


def fin():
    GPIO.cleanup()

def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)

def start():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    GPIO.setup(enb,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
    
def avance(nb):

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    sleep(0.1 * nb)

    stop()
    
    
    
start()

p=GPIO.PWM(ena,1000)
q=GPIO.PWM(enb,1000)
p.start(25)
q.start(25)

p.ChangeDutyCycle(100)
q.ChangeDutyCycle(100)

avance(3)
fin()
