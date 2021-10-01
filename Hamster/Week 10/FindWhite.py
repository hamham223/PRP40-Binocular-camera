import cv2
import copy
img=cv2.imread("cube.jpg")
#imgGray=cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)

def judge(x,y):
    red=copy.copy(img[x][y][0])
    green=copy.copy(img[x][y][1])
    blue=copy.copy(img[x][y][2])
    dis=(255-red)+(255-green)+(255-blue)
    if dis<=50: return 1
    else : return 0


u=len(img)
v=len(img[0])
for i in range(0,u):
    for j in range(0,v):
        if judge(i,j)==1:  
            img[i][j]=[0,255,0]

cv2.imwrite("white.jpg",img)