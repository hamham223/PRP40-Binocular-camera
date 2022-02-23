import cv2
import numpy as np
import matplotlib.pyplot as plt

def if_blue(color):
    if (color[0]>=180 )& (color[2]<=30): return True
    orange=[165,60,0]
    diff=abs(int(color[2])-int(orange[2]))*0.1+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.6
    threshold=45
    return (diff<=threshold)

img=cv2.imread("Left_8.jpg")
img_mark=cv2.imread("Left_8.jpg")
#HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#print(HSV_img[1470][783])
#print(img[1470][783])
for i in range(0,1520):
    for j in range(0,1520):
        if if_blue(img[i][j]):
            cv2.circle(img_mark,(j,i),1,(0,255,0),1)
cv2.imwrite("blue_find.jpg",img_mark)
plt.imshow(img_mark),plt.show()