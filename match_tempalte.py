from ast import While
import cv2
from cv2 import circle
import numpy as np
import draw_engine as de
from PIL import Image,ImageEnhance

search_size = 1080
from mss import mss
left = int((1920/2)-(search_size/2))
upper = int((1080/2)-(search_size/2))

mon = {'top': upper, 'left':left, 'width':search_size, 'height':search_size}
sct = mss()
img_rgb = cv2.imread('teste2.jpg')
sct_img = sct.grab(mon)
img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
img_rgb = np.asarray(img)

template = cv2.imread('temp.jpg')
w, h = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)

circles = []

for pt in zip(*loc[::-1]):  # Switch collumns and rows
    if pt[0] < 1080 and pt[1] < 1080:
        # print(pt)
        start = de.e_pixel(0,0,"red")
        end = de.e_pixel(int(search_size/2)+pt[0],pt[1],"red")
        circles.append(de.line(start,end))
    
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

print("drawing")
while True:
    for i in circles:
        i.draw()
    # for i in circles:
    #     i.clean()
        

cv2.imwrite('result.png', img_rgb)

# a = e_pixel()
# b = e_pixel()
# a.x = 100
# a.y = 100
# b.x = 1920
# b.y = 1080
# ed = line(a,b)
# ed.draw()


# a = e_pixel()
# a.x = 1920 / 2
# a.y = 1080 / 2
# ed = circle(a,25)


# a = e_pixel()
# a.x = 1920 / 2
# a.y = 1080 / 2
# ed = circle(a,25)

# while True:
#     de.circle()