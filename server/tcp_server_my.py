#!/usr/bin/env python
# Redesigned for compactness, clarity, consistency and expandability
# by Guenter Huber 2018-05
import RPi.GPIO as GPIO
import steer    # better name than car_dir! car_directory? direction!
import motor_my as motor
from socket import * # why *?
from time import ctime

# Avoid local constants that add no value as Py has no C macros or text replacement anyway
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# bind takes a tuple / pair (in brackets) as argument
tcpSerSock.bind(('', 21567)) # arg 1: empty string becomes host address; arg 2: port
tcpSerSock.listen(5)         # max number of connections permitted at one time

steer.setup(busnum=1) # 0 if Pi 0 or 1
motor.setup(busnum=1)
steer.home()

run = True
while run:
    print 'Waiting for connection...'
    # upon connect accept() returns a socket for comm; by default accept() is blocking
    # tcpSerSock.accept() returns a pair of values into tcpCliSock, client
    tcpCliSock, client = tcpSerSock.accept() # variables addr for client and ADDR for server very bad
    print 'Connected from: ', client

    while run:
        data = ''
        data = tcpCliSock.recv(1024) # argument: buffersize
        print 'data: ', data # ONE print for data; use extra ones in elif to debug ==
        if not data:
            break
        elif data == 'quit':
            motor.ctrl(0) # stop car before stopping server
            steer.home() # set steering to straight ahead to help calibration after power cycle
            run = False
            break
        elif data == 'bye':
            motor.ctrl(0)
            steer.home()
            print 'Client just gracefully quit. Bye!'
            break
        elif data == 'forward':
            motor.forward()
        elif data == 'backward':
            motor.backward()
        elif data == 'left':
            steer.turn_left()
        elif data == 'right':
            steer.turn_right()
        elif data == 'home':
            steer.home()
        elif data == 'stop':
            motor.ctrl(0)
        elif data == 'read cpu temp':
            temp = cpu_temp.read()
            tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
        elif data[0:5] == 'speed':     # Change the speed
            numLen = len(data) - len('speed')
            if numLen == 1 or numLen == 2 or numLen == 3:
                tmp = data[-numLen:]
                print 'tmp(str) = %s' % tmp
                spd = int(tmp)
                print 'spd(int) = %d' % spd
                if spd < 24:
                    spd = 24
                motor.setSpeed(spd)
        elif data[0:5] == 'turn=':    # Turning Angle
            angle = data.split('=')[1]
            try:
                angle = int(angle)
                steer.turn(angle)
            except:
                print 'Error: angle =', angle
        elif data[0:8] == 'forward=':
            spd = data[8:]
            try:
                spd = int(spd)
                motor.forward(spd)
            except:
                print 'Error speed =', spd
        elif data[0:9] == 'backward=': #indentation screwed up
            spd = data.split('=')[1]
            try:
                spd = int(spd)
                motor.backward(spd)
            except:
                print 'Error: speed =', spd

        else:
            print 'Command ' + data + ' unknown'

tcpSerSock.close()
print 'tcpSerSock closed. Server stopped.'
