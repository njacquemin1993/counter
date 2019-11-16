#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageTk
from datetime import datetime
import numpy
import sys, os
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
    import tkFont
else:
    import tkinter, tkinter.font as tkFont

import RPi.GPIO as GPIO

root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='black')
canvasImage = None

#Load background
img = Image.open('BackgroundCompteurShots.png')
imgWidth, imgHeight = img.size
ratio = min(float(w)/imgWidth, float(h)/imgHeight)
imgWidth = int(imgWidth*ratio)
imgHeight = int(imgHeight*ratio)
img = img.resize((imgWidth,imgHeight), Image.ANTIALIAS)
image = ImageTk.PhotoImage(img)
canvasImage = canvas.create_image(w/2,h/2,image=image)
counterText = canvas.create_text(w/2, h/2, text=" 0 ", fill="#fab150", font=("SYEMOX italic", 140,"normal" ))
canvas.create_text(w/2, 3*h/4, text=u"shots servis depuis le début de la soirée", fill="#fab150", font=("SYEMOX italic", 90,"normal" ))

counter = 0

while True:
    canvas.itemconfigure(counterText, text=" {} ".format(counter))
    root.update_idletasks()
    root.update()
    # wait for gpio
    GPIO.setmode(GPIO.BCM)
    # GPIO 23 set up as input. It is pulled up to stop false signals
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # connect GPIO port 23 (pin 16) to GND (pin 6)
    try:
        print("Wait GPIO: {0}".format(datetime.now()))
        GPIO.wait_for_edge(23, GPIO.FALLING)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
    print("Cleanup GPIO: {0}".format(datetime.now()))
    GPIO.cleanup()
    counter += 1
