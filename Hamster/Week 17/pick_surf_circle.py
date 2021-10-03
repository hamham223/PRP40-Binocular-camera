import math
import cv2
import numpy as np
import find_houghcircle
import mySURF
def judge(img,keypoints1,count,circles):
    n=0
    key=[]
    for i in range(0,len(keypoints1)):
        xk=float(keypoints1[i].pt[0])
        yk=float(keypoints1[i].pt[1])
        boo=0
        for j in range(0,count):
            xh=float(circles[0][j][0])#xh stands for the x coordinate of the hough circle
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

d1=[]
d2=[]   
key1=judge(mySURF.img1,mySURF.k1,find_houghcircle.count1,find_houghcircle.circles1)
cv_kpts1 = [cv2.KeyPoint(mySURF.k1[key1[i]].pt[0], mySURF.k1[key1[i]].pt[1], 
    mySURF.k1[key1[i]].size, mySURF.k1[key1[i]].angle, mySURF.k1[key1[i]].response, 
    mySURF.k1[key1[i]].octave, mySURF.k1[key1[i]].class_id)
    for i in range(0,len(key1))]
for i in range(0,len(key1)):
    d1.append(mySURF.descriptor1[key1[i]])

key2=judge(mySURF.img2,mySURF.k2,find_houghcircle.count2,find_houghcircle.circles2)
cv_kpts2 = [cv2.KeyPoint(mySURF.k2[key2[i]].pt[0], mySURF.k2[key2[i]].pt[1], 
    mySURF.k2[key2[i]].size, mySURF.k2[key2[i]].angle, mySURF.k2[key2[i]].response, 
    mySURF.k2[key2[i]].octave, mySURF.k2[key2[i]].class_id)
    for i in range(0,len(key2))]
for i in range(0,len(key2)):
    d2.append(mySURF.descriptor2[key2[i]])

d1=np.array(d1)
d2=np.array(d2)