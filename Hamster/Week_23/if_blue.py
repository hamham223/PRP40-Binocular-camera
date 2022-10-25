import cv2
import numpy  as np

def if_blue(color):
    if (color[0]>=180 )& (color[2]<=30): return True
    orange=[165,60,0]
    diff=abs(int(color[2])-int(orange[2]))*0.1+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.6
    threshold=45
    return (diff<=threshold)

img1 = cv2.imread('Left_8.jpg')
img2 = cv2.imread('Right_8.jpg')
Blank = np.ones((1520,1520,3),dtype=np.uint8)
Blank = Blank*255
for i in range(0,1520):
    for j in range(0,1520):
        if if_blue(img1[i,j]):
            cv2.circle(Blank,(j,i),1,(0,255,0),1)
cv2.imwrite("wuwu.jpg",Blank)