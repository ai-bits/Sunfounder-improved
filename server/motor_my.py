#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCA9685 as controller
import time

# Raspberry Pi pin11, 12, 13 & 15 motor direction counter-/clockwise
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# Set channel 4 & 5 of the servo driver IC to generate PWM for speed control
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]

# Adjust servo driver IC PWM duty cycle for channel 4 & 5 for speed control
def setSpeed(speed):
    speed *= 40
    print 'speed is: ', speed
    pwm.write(EN_M0, 0, speed)
    pwm.write(EN_M1, 0, speed)

def setup(busnum=None):
    global forward0, forward1, backward1, backward0
    global pwm
    if busnum == None:
        pwm = controller.PWM() # Initialize servo controller
    else:
        pwm = controller.PWM(bus_number=busnum)

    pwm.frequency = 60
    forward0 = 'True'
    forward1 = 'True'
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) # Number GPIOs by physical location
    try:
        for line in open("config"):
            if line[0:8] == "forward0":
                forward0 = line[11:-1]
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
    except:
        pass
    if forward0 == 'True':
        backward0 = 'False'
    elif forward0 == 'False':
        backward0 = 'True'
    if forward1 == 'True':
        backward1 = 'False'
    elif forward1 == 'False':
        backward1 = 'True'
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output

# Control the DC motor to rotate clockwise / fwd

def motor0(x):
    if x == 'True':
        GPIO.output(Motor0_A, GPIO.LOW)
        GPIO.output(Motor0_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor0_A, GPIO.HIGH)
        GPIO.output(Motor0_B, GPIO.LOW)
    else:
        print 'Config Error'

def motor1(x):
    if x == 'True':
        GPIO.output(Motor1_A, GPIO.LOW)
        GPIO.output(Motor1_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor1_A, GPIO.HIGH)
        GPIO.output(Motor1_B, GPIO.LOW)

def forward():
    motor0(forward0)
    motor1(forward1)

def backward():
    motor0(backward0)
    motor1(backward1)

def forwardWithSpeed(spd = 50):
    setSpeed(spd)
    motor0(forward0)
    motor1(forward1)

def backwardWithSpeed(spd = 50):
    setSpeed(spd)
    motor0(backward0)
    motor1(backward1)

def stop():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

# parameter 1 status: stop or move; parm 2 direction fwd or bck
def ctrl(status, direction=1):
    if status == 1:   # move
        if direction == 1:     # Forward
            forward()
        elif direction == -1:  # Backward
            backward()
        else:
            print 'Argument error! direction must be 1 or -1.'
    elif status == 0: # stop
        stop()
    else:
        print 'Argument error! status must be 0 or 1.'

def test():
    while True:
        setup()
        ctrl(1)
        time.sleep(3)
        setSpeed(10)
        time.sleep(3)
        setSpeed(100)
        time.sleep(3)
        ctrl(0)

if __name__ == '__main__':
    setup()
    setSpeed(50)
    #forward()
    #backward()
    stop()
