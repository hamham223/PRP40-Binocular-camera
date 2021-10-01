import cv2
import numpy as np
import copy
import houghcircle
import math
def judge(keypoints1):
    n=0
    k=keypoints1
    key=[]
    for i in range(0,len(keypoints1)):
        #k=copy.copy(keypoints1[i])
        xk=float(keypoints1[i].pt[0])
        yk=float(keypoints1[i].pt[1])
        boo=0
        for j in range(0,houghcircle.count):
            xh=float(houghcircle.circles[0][j][0])
            yh=float(houghcircle.circles[0][j][1])
            rh=float(houghcircle.circles[0][j][2])
            dis=math.sqrt(float((xk-xh)**2+(yk-yh)**2))
            if abs(dis-rh)<=6:
                boo=1
                break
        if boo==1:
            key.append(i)
            n=n+1
    return key
img1 = cv2.imread('left1.jpg',cv2.IMREAD_GRAYSCALE)
image1=copy.copy(img1)
#创建一个SURF对象
surf = cv2.xfeatures2d.SURF_create()
#SIFT对象会使用Hessian算法检测关键点，并且对每个关键点周围的区域计算特征向量。该函数返回关键点的信息和描述符
k1,descriptor1 = surf.detectAndCompute(image1,None)

key=judge(k1)
cv_kpts1 = [cv2.KeyPoint(k1[key[i]].pt[0], k1[key[i]].pt[1], 
    k1[key[i]].size, k1[key[i]].angle, k1[key[i]].response, k1[key[i]].octave, k1[key[i]].class_id)
    for i in range(0,len(key))]
#image1 = cv2.drawKeypoints(image=image1,keypoints = cv_kpts1, 
#outImage=image1,color=(0,255,0))
image1 = cv2.drawKeypoints(image=image1,keypoints = cv_kpts1, 
outImage=image1,color=(0,255,0),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite('surf.jpg',image1)
