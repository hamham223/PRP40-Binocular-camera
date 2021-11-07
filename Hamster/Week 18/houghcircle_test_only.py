import cv2
import math
import numpy as np
#pi=3.1415926
import matplotlib.pyplot as plt

def calc_median_color(img,x_0,y_0,r):
    count=0;color=np.zeros((3),dtype=np.uint0)
    #print(img.shape)
    #print(x_0,y_0,r)
    for i_ in range(x_0-r,x_0+r):
        for j_ in range(y_0-r,y_0+r):
            if (i_>=1200)|(j_>=1600): continue
            dis=math.sqrt(float((i_-x_0)**2+(j_-y_0)**2))
            if dis<=r:
                count=count+1
                #print(i_,j_)
                color[0]=color[0]+np.uint0(img[i_,j_,0])
                color[1]=color[1]+np.uint0(img[i_,j_,1])
                color[2]=color[2]+np.uint0(img[i_,j_,2])
   # print(count)
    if (count!=0):
        color[0]=int(color[0]/count)
        color[1]=int(color[1]/count)
        color[2]=int(color[2]/count)
    return [int(x) for x in color]

img = cv2.imread('Model1.jpg')

img = cv2.resize(img,dsize=(1600,1200))

img = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
 
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 80,
                           param1=20, param2=10, minRadius=10,maxRadius=30)
circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    m_color_1=calc_median_color(img,i[1],i[0],i[2])
    if ((m_color_1[0]>=160)&(m_color_1[0]<=185)):
        cv2.circle(img, (i[1], i[0]), i[2], (0, 255, 0), 2)
        cv2.circle(img, (i[1], i[0]), 2, (0, 255, 0), 3)
    #print(i[0],i[1])
plt.imshow(img),plt.show()
