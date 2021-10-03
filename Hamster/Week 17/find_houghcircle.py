import cv2
import numpy as np
import math

def findcircle(x,y,c,circles):
    for j in range(0,c):
        xh=float(circles[0][j][0])
        yh=float(circles[0][j][1])
        rh=float(circles[0][j][2])
        dis=math.sqrt(float((x-xh)**2+(y-yh)**2))
        if abs(dis-rh)<=6:
            return circles[0][j][0],circles[0][j][1],rh
    return -1,-1,-1

def Hough(str1):
    img = cv2.imread(str1)
    img = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)
    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
                           param1=40, param2=20, minRadius=19,maxRadius=77)
    circles = np.uint16(np.around(circles))
    count=len(circles[0])
    return circles,count

circles1, count1= Hough('Left3.jpg') 
circles2, count2= Hough('Right3.jpg')
