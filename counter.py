#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2
import numpy
import sys, os
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

import RPi.GPIO as GPIO

root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='black')

def showPIL(pilImage):
    imgWidth, imgHeight = pilImage.size
    # resize photo to full screen
    ratio = min(float(w)/imgWidth, float(h)/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update_idletasks()
    root.update()

counter = 0

while True:
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
    GPIO.setmode(GPIO.BCM)
    # GPIO 23 set up as input. It is pulled up to stop false signals
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # connect GPIO port 23 (pin 16) to GND (pin 6)
    try:
        GPIO.wait_for_edge(23, GPIO.FALLING)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
    GPIO.cleanup()
    counter += 1
