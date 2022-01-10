import cv2
import numpy as np
import matplotlib.pyplot as plt

def if_orange(color):
    orange=[3,151,248]
    diff=abs(int(color[2])-int(orange[2]))*0.6+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.1
    threshold=30
    return (diff<=threshold)

img=cv2.imread("Left_1.jpg")
img_mark=cv2.imread("Left_1.jpg")

for i in range(0,1520):
    for j in range(0,1520):
        if if_orange(img[i][j]):
            cv2.circle(img_mark,(j,i),1,(0,255,0),1)
cv2.imwrite("orange_find.jpg",img_mark)
plt.imshow(img_mark),plt.show()