import cv2
import numpy as np
import matplotlib.pyplot as plt

def if_blue(color):
    if (color[0]>=180 )& (color[2]<=30): return True
    orange=[165,60,0]
    diff=abs(int(color[2])-int(orange[2]))*0.1+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.6
    threshold=30
    return (diff<=threshold)

img=cv2.imread("Left_1.jpg")
img_mark=cv2.imread("Left_1.jpg")

for i in range(0,1520):
    for j in range(0,1520):
        if if_blue(img[i][j]):
            cv2.circle(img_mark,(j,i),1,(0,255,0),1)
cv2.imwrite("blue_find.jpg",img_mark)
plt.imshow(img_mark),plt.show()