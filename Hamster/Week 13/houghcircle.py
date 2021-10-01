import cv2

import numpy as np


img = cv2.imread('LEFT_1.jpg')
img = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
 
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100,
                           param1=40, param2=20, minRadius=20,maxRadius=70)
circles = np.uint16(np.around(circles))
count=len(circles[0])


f=open("circles-Right.txt",'w')
for i in circles[0, :]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(img, (i[0], i[1]), 2, (0, 255, 0), 3)
    f.write(str(i[0])+" "+str(i[1])+"\n")

cv2.imwrite('Hough_RIGHT.jpg',img)


