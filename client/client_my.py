#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Revised for compactness (Removed 'Duh' comments and print statements), clarity,..
# by Guenter Huber 2018-05
from Tkinter import * # Python interface to Tcl/Tk #Spyder started from Sunfounder env. Why warning!?
from socket import *  # Tkinter & socket definitely installed

# Avoid local constants that add no value as Py has no C macros or text replacement anyway
tcpCliSock = socket(AF_INET, SOCK_STREAM)
# connect takes a tuple / pair (that's why the extra brackets) as argument
tcpCliSock.connect(('10.0.0.8', 21567))   # args: host to connect to, port

top = Tk() # Create top window
top.title('Sunfounder Raspberry Pi Smart Video Car')
# Didn't dig deeper into Tk. Is its own science.
def forward_fun(event): # Separate func for each button seems inelegant. What is the arg for then?
    tcpCliSock.send('forward') # Crude commands limit functionality
    # As the socket needs a string anyway I'd combine control cmd and value (speed, steering angle)
def backward_fun(event):
    tcpCliSock.send('backward')

def left_fun(event):
    tcpCliSock.send('left')

def right_fun(event):
    tcpCliSock.send('right')

def stop_fun(event):
    tcpCliSock.send('stop')

def home_fun(event):
    tcpCliSock.send('home')

def server_quit(event): # stops tcp_server_my.py for graceful exit
    tcpCliSock.send('quit')

def quit_fun(event):
    # tcpCliSock.send('stop') # and 'home' moved to tcp_server_my.py
    tcpCliSock.send('bye')
    tcpCliSock.close()
    top.destroy() #quit() doesn't. It actually hangs the app

Btn0 = Button(top, width=8, text='Fwd=W') # Added shortcut key to button labels
Btn1 = Button(top, width=8, text='S=Bwd')
Btn2 = Button(top, width=8, text='A=Left')
Btn3 = Button(top, width=8, text='Right=D')
Btn4 = Button(top, width=8, text='Quit')
Btn5 = Button(top, width=8, height=2, text='Home')
Btn6 = Button(top, width=8, text='Quit Server') # Added to close server socket cleanly. Needs tweak in tcp_server_my.py
Btn7 = Button(top, width=8, text='Stop') # Added to tame motor running wild in testing

Btn0.grid(row=0,column=1)
Btn1.grid(row=2,column=1)
Btn2.grid(row=1,column=0)
Btn3.grid(row=1,column=2)
Btn4.grid(row=3,column=2)
Btn5.grid(row=1,column=1)
Btn6.grid(row=3,column=0)
Btn7.grid(row=3,column=1)

Btn0.bind('<ButtonPress-1>', forward_fun)
Btn1.bind('<ButtonPress-1>', backward_fun)
Btn2.bind('<ButtonPress-1>', left_fun)
Btn3.bind('<ButtonPress-1>', right_fun)
Btn4.bind('<ButtonPress-1>', quit_fun) # No need to wait for release of button to quit
Btn6.bind('<ButtonPress-1>', server_quit)
Btn7.bind('<ButtonPress-1>', stop_fun)
Btn0.bind('<ButtonRelease-1>', stop_fun)
Btn1.bind('<ButtonRelease-1>', stop_fun)
Btn2.bind('<ButtonRelease-1>', home_fun)
Btn3.bind('<ButtonRelease-1>', home_fun)
Btn5.bind('<ButtonRelease-1>', home_fun)

# Bind the keys to the corresponding callback function
top.bind('<KeyPress-w>', forward_fun)
top.bind('<KeyPress-s>', backward_fun)
top.bind('<KeyPress-a>', left_fun)
top.bind('<KeyPress-d>', right_fun)
top.bind('<KeyPress-h>', home_fun)
top.bind('<KeyRelease-a>', home_fun)
top.bind('<KeyRelease-d>', home_fun)
top.bind('<KeyRelease-s>', stop_fun)
top.bind('<KeyRelease-w>', stop_fun)

# Removed camera control, because for lane detection the camera is mounted statically

spd = 50

def changeSpeed(ev=None):
    # tmp = 'speed' # Why the heck need to go via tmp?
    global spd
    spd = speed.get()
    data = 'speed' + str(spd) # tmp + str(spd)
    print 'send(data) = %s' % data
    tcpCliSock.send(data)

label = Label(top, text='Speed:', fg='red')
label.grid(row=6, column=0)

speed = Scale(top, from_=0, to=100, orient=HORIZONTAL, command=changeSpeed)
speed.set(50)
speed.grid(row=6, column=1)

def main():
    top.mainloop()

if __name__ == '__main__':
    main()
