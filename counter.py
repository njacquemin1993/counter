#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageTk
from datetime import datetime
import numpy
import sys, os
import time
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
    import tkFont
else:
    import tkinter, tkinter.font as tkFont
import RPi.GPIO as GPIO

# Listener for GPIO
def onButtonPress(channel):
    global counter
    global update
    if GPIO.input(23):
        # Double check it's a rising edge
        counter += 1
        update = True

# Setup variables
filepath = "/home/pi/counter/counter.txt"
update = False
try:
    with open(filepath) as f:
        counter = int(f.readlines()[0])
except:
    counter = 0

# Load background
img = Image.open('/home/pi/counter/BackgroundCompteurShots.png')

# Setup TKinter
root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
canvas = tkinter.Canvas(root,width=w,height=h, highlightthickness=0)
canvas.pack()
canvas.configure(background='black')
imgWidth, imgHeight = img.size
ratio = min(float(w)/imgWidth, float(h)/imgHeight)
imgWidth = int(imgWidth*ratio)
imgHeight = int(imgHeight*ratio)
img = img.resize((imgWidth,imgHeight), Image.ANTIALIAS)
image = ImageTk.PhotoImage(img)
canvas.create_image(w/2,h/2,image=image)
counterText = canvas.create_text(w/2, 7*h/20, text=" {0} ".format(counter), fill="#fab150", font=("SYEMOX italic", 200,"normal"))
canvas.create_text(w/2, 3*h/4, text=u"shots servis", fill="#fab150", font=("SYEMOX italic", 150, "normal"))
root.update_idletasks()
root.update()

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=onButtonPress, bouncetime=50)

# Infinite loop until keyboard interrupt
try:
    while True:
        time.sleep(0.1)
        if update:
            update = False
            canvas.itemconfigure(counterText, text=" {} ".format(counter))
            root.update_idletasks()
            root.update()
            with open(filepath, "w") as f:
                f.write("{0}".format(counter))

except KeyboardInterrupt:
    pass

# Clean exit
GPIO.cleanup()
