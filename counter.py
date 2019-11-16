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

print(tkFont.names())


def showPIL(pilImage):
    global canvasImage
    print("Enter show pil: {0}".format(datetime.now()))
    imgWidth, imgHeight = pilImage.size
    print(imgWidth, imgHeight)
    # resize photo to full screen
    ratio = min(float(w)/imgWidth, float(h)/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    print(imgWidth, imgHeight)
    print("Resize: {0}".format(datetime.now()))
#    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    print("Photo image: {0}".format(datetime.now()))
    image = ImageTk.PhotoImage(pilImage)
    print("Create image: {0}".format(datetime.now()))
    if canvasImage == None:
        canvasImage = canvas.create_image(w/2,h/2,image=image)
    else:
        canvas.itemconfig(canvasImage, image=image)
    label = canvas.create_text(w/2, h/2, text="Test", fill="#ffab15", font=("SYEMOX italic",50 ,"bold" ))
    print("Update idle: {0}".format(datetime.now()))
    root.update_idletasks()
    print("Update: {0}".format(datetime.now()))
    root.update()
    print("Quit show pil: {0}".format(datetime.now()))

counter = 0

while True:
    print("Prepare image: {0}".format(datetime.now()))
    img = Image.open('BackgroundCompteurShots.png')
    number = str(counter)
    text = u"shots servis depuis le début de la soirée"

    fnt_n = ImageFont.truetype('./Syemox.ttf', 150)
    fnt_t = ImageFont.truetype('./Syemox.ttf', 120)
    d = ImageDraw.Draw(img)
    width_n, height_n = d.textsize(number, font=fnt_n)
    width_t, height_t = d.textsize(text, font=fnt_t)
    center_x = 1920 / 2
    center_y = 650
    margin_y = 70
    color = (250, 177, 80)
    pos_n_x = center_x - width_n / 2
    pos_n_y = center_y - (height_n + height_t + margin_y) / 2
    pos_t_x = center_x - width_t / 2
    pos_t_y = pos_n_y + height_n + margin_y
    d.text((pos_n_x, pos_n_y), number, font=fnt_n, fill=color)
    d.text((pos_t_x, pos_t_y), text, font=fnt_t, fill=color)
    showPIL(img)
    # wait for gpio
    print("Config GPIO: {0}".format(datetime.now()))
    GPIO.setmode(GPIO.BCM)
    # GPIO 23 set up as input. It is pulled up to stop false signals
    print("Setup GPIO: {0}".format(datetime.now()))
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
