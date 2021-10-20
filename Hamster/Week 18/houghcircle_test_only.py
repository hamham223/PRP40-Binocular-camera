import cv2
#import math
import numpy as np
#pi=3.1415926
import matplotlib.pyplot as plt
 
img = cv2.imread('Right3.jpg')
#img = cv2.resize(img,dsize=(1000,500))
img = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
 
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
                           param1=40, param2=20, minRadius=19,maxRadius=95)
circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(img, (i[0], i[1]), 2, (0, 255, 0), 3)
    print(i[0],i[1])
 
plt.imshow(img),plt.show()
