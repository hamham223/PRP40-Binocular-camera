import cv2
import numpy as np
import copy

img1 = cv2.imread('model.jpg',cv2.IMREAD_GRAYSCALE)
image1=copy.copy(img1)
#创建一个SURF对象
surf = cv2.xfeatures2d.SURF_create()
#SIFT对象会使用Hessian算法检测关键点，并且对每个关键点周围的区域计算特征向量。该函数返回关键点的信息和描述符
keypoints1,descriptor1 = surf.detectAndCompute(image1,None)
#image1 = cv2.drawKeypoints(image=image1,keypoints = keypoints1, 
#outImage=image1,color=(0,255,0),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
image1 = cv2.drawKeypoints(image=image1,keypoints = keypoints1, 
outImage=image1,color=(0,255,0))
cv2.imshow('surf_keypoints1',image1)
cv2.waitKey(10000)
cv2.destroyAllWindows()