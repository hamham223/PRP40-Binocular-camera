import cv2
#import math
import numpy as np
#pi=3.1415926

 
img = cv2.imread('left1.jpg')
img = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
 
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30,
                           param1=50, param2=25, minRadius=19,maxRadius=66)
circles = np.uint16(np.around(circles))
count=0
f=open("circles.txt",'w')
for i in circles[0, :]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(img, (i[0], i[1]), 2, (0, 255, 0), 3)
    f.write(str(i[0])+" "+str(i[1])+"\n")
    count=count+1

cv2.imwrite('Final-left.jpg',img)
