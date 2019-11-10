from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy

counter = 0

while True:
    img = Image.open('BackgroundCompteurShots.png')
    number = str(counter)
    text = "shots servis depuis le début de la soirée"

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

    opencvImage = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", opencvImage)
    if cv2.waitKey(0) == 27:
        break
    counter += 1
