import mySURF
import pandas as pd
import numpy as np 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2

def getX(goodMatchePoints,k1,k2):
    XList=[];YList=[]
    for i in goodMatchePoints:
        left_id=i.queryIdx
        right_id=i.trainIdx
        xl=int(k1[left_id].pt[0])
        yl=int(k1[left_id].pt[1])
        xr=int(k2[right_id].pt[0])
        yr=int(k2[right_id].pt[1])
        XList.append([xl,yl])
        YList.append([xr,yr])
    return XList,YList

cluster =  20

X,Y = getX(mySURF.goodMatchePoints,mySURF.k1,mySURF.k2)
Kmean_X = KMeans(n_clusters=cluster).fit(X)
Kmean_Y = KMeans(n_clusters=cluster).fit(Y)

Blank  =np.zeros((1520,3040,3),dtype=np.uint8)

for i in Kmean_X.cluster_centers_:
    cv2.circle(Blank,(int(i[0]),int(i[1])),50,(0,255,255),3)

for i in Kmean_Y.cluster_centers_:
    cv2.circle(Blank,(int(i[0])+1520,int(i[1])),50,(0,255,255),3)

for i in X:
    cv2.circle(Blank,(int(i[0]),int(i[1])),5,(0,255,0),-1)
for i in Y:
    cv2.circle(Blank,(int(i[0])+1520,int(i[1])),5,(0,255,0),-1)

exists_ = np.zeros(cluster,dtype=bool)
match = []
for i in range(len(X)):
    if exists_[Kmean_X.labels_[i]]: continue
    exists_[Kmean_X.labels_[i]]=True
    j = Kmean_X.labels_[i]
    k = Kmean_Y.labels_[i]
    match.append([j,k])
    pt1 = (int(Kmean_X.cluster_centers_[j][0]),int(Kmean_X.cluster_centers_[j][1]))
    pt2 = (int(Kmean_Y.cluster_centers_[k][0]+1520),int(Kmean_Y.cluster_centers_[k][1]))
    cv2.line(Blank,pt1,pt2,(255,255,0),2)
cv2.imwrite("Kmeans.jpg",Blank)

np.save("ML_left",Kmean_X.cluster_centers_)
np.save("ML_right",Kmean_Y.cluster_centers_)
np.save("ML_match",match)