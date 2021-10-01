import cv2
import numpy as np
import copy
import math

img1 = cv2.imread('Left.jpg',cv2.IMREAD_GRAYSCALE)
surf = cv2.xfeatures2d.SURF_create() #create a SURF object
k1,descriptor1 = surf.detectAndCompute(img1,None)

def Hough(str1):
    img = cv2.imread(str1)
    img = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)
    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30,
                           param1=50, param2=25, minRadius=19,maxRadius=66)
    circles = np.uint16(np.around(circles))
    count=len(circles[0])
    return circles,count

circles1, count1= Hough('Left.jpg') 

def judge(img1,keypoints1,count,circles):
    n=0
    key=[]
    for i in range(0,len(keypoints1)):
        xk=float(keypoints1[i].pt[0])
        yk=float(keypoints1[i].pt[1])
        boo=0
        if abs(img1[int(xk)][int(yk)]-112)<4:
            continue
        if abs(img1[int(xk)][int(yk)]-128)<3:
            continue
        for j in range(0,count):
            xh=float(circles[0][j][0])
            yh=float(circles[0][j][1])
            rh=float(circles[0][j][2])
            dis=math.sqrt(float((xk-xh)**2+(yk-yh)**2))
            if abs(dis-rh)<=6:
                boo=1
                break
        if boo==1:
            key.append(i)
            n=n+1
    return key

def findcircle(x,y,c,circles):
    for j in range(0,c):
        xh=float(circles[0][j][0])
        yh=float(circles[0][j][1])
        rh=float(circles[0][j][2])
        dis=math.sqrt(float((x-xh)**2+(y-yh)**2))
        if abs(dis-rh)<=6:
            return circles[0][j][0],circles[0][j][1]
    return -1,-1

d1=[]  
key1=judge(img1,k1,count1,circles1)
cv_kpts1 = [cv2.KeyPoint(k1[key1[i]].pt[0], k1[key1[i]].pt[1], 
    k1[key1[i]].size, k1[key1[i]].angle, k1[key1[i]].response, k1[key1[i]].octave, k1[key1[i]].class_id)
    for i in range(0,len(key1))]
for i in range(0,len(key1)):
    d1.append(descriptor1[key1[i]])

image1=copy.copy(img1)
image1 = cv2.drawKeypoints(image=img1,keypoints = cv_kpts1, 
outImage=image1, color=(0,255,0))
cv2.imwrite('Surf_Hough_Color.jpg',image1)

#f=open('Feature_Points.txt','w')
#f.write("  x      y         \n")
#for i in range(0,len(key1)):
#    xxx=int(k1[key1[i]].pt[0])
#    yyy=int(k1[key1[i]].pt[1])
#    f.write(str(xxx)+"   "+str(yyy)+"     ")
#    f.write(str(img1[xxx][yyy])+"\n")
#f.close()
print(img1[567][963])