import cv2
import numpy as np
import copy
import math

img1 = cv2.imread('Left.jpg',cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Right.jpg',cv2.IMREAD_GRAYSCALE)

surf = cv2.xfeatures2d.SURF_create() #create a SURF object

k1,descriptor1 = surf.detectAndCompute(img1,None)
k2,descriptor2 = surf.detectAndCompute(img2,None)

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
circles2, count2= Hough('Right.jpg')

def judge(img,keypoints1,count,circles):
    n=0
    key=[]
    for i in range(0,len(keypoints1)):
        xk=float(keypoints1[i].pt[0])
        yk=float(keypoints1[i].pt[1])
        boo=0
        if abs(img[int(xk)][int(yk)]-112)<4:
            continue
        if abs(img[int(xk)][int(yk)]-128)<3:
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
            return circles[0][j][0],circles[0][j][1],rh
    return -1,-1,-1
d1=[]
d2=[]   
key1=judge(img1,k1,count1,circles1)
cv_kpts1 = [cv2.KeyPoint(k1[key1[i]].pt[0], k1[key1[i]].pt[1], 
    k1[key1[i]].size, k1[key1[i]].angle, k1[key1[i]].response, k1[key1[i]].octave, k1[key1[i]].class_id)
    for i in range(0,len(key1))]
for i in range(0,len(key1)):
    d1.append(descriptor1[key1[i]])

key2=judge(img2,k2,count2,circles2)
cv_kpts2 = [cv2.KeyPoint(k2[key2[i]].pt[0], k2[key2[i]].pt[1], 
    k2[key2[i]].size, k2[key2[i]].angle, k2[key2[i]].response, k2[key2[i]].octave, k2[key2[i]].class_id)
    for i in range(0,len(key2))]
for i in range(0,len(key2)):
    d2.append(descriptor2[key2[i]])

d1=np.array(d1)
d2=np.array(d2)
matcher = cv2.FlannBasedMatcher()
matchePoints = matcher.match(d1,d2)

#提取强匹配特征点
minMatch = 1
maxMatch = 0
for i in range(len(matchePoints)):
    if minMatch > matchePoints[i].distance:
        minMatch = matchePoints[i].distance
    if maxMatch < matchePoints[i].distance:
        maxMatch = matchePoints[i].distance
print('最佳匹配值是:',minMatch)
print('最差匹配值是:',maxMatch)
goodMatchePoints = []
files=open("match_result.txt",'w')
files.write("x_L "+"y_L        x_R y_R      "
                + " H_x_L H_y_L      H_x_R H_y_R    R "+"\n")
xl=[];yl=[];xr=[];yr=[];xhl=[];yhl=[];xhr=[];yhr=[];rl=[];rr=[]
for i in range(len(matchePoints)):
    if matchePoints[i].distance < minMatch + (maxMatch-minMatch)/16:
        left_id=matchePoints[i].queryIdx
        right_id=matchePoints[i].trainIdx
        xl_temp=k1[key1[left_id]].pt[0]
        yl_temp=k1[key1[left_id]].pt[1]
        xr_temp=k2[key2[right_id]].pt[0]+1520
        yr_temp=k2[key2[right_id]].pt[1]
        if abs(float(yr_temp-yl_temp)/float(xr_temp-xl_temp))<0.03:
            goodMatchePoints.append(matchePoints[i])
            xhl_temp,yhl_temp,rl_temp=findcircle(xl_temp,yl_temp,count1,circles1)
            xhr_temp,yhr_temp,rr_temp=findcircle(xr_temp-1520,yr_temp,count2,circles2)
            xhr_temp=xhr_temp+1520
            xl.append(int(xl_temp));yl.append(int(yl_temp))
            xr.append(int(xr_temp));yr.append(int(yr_temp))
            xhl.append(xhl_temp);yhl.append(yhl_temp)
            xhr.append(xhr_temp);yhr.append(yhr_temp)
            rl.append(rl_temp);rr.append(rr_temp)
#sort
for i in range(len(goodMatchePoints)-1):
    for j in range(i+1,len(goodMatchePoints)-1):
        if xhl[j]<xhl[i]:
            temp=xhl[j];xhl[j]=xhl[i];xhl[i]=temp
            temp=yhl[j];yhl[j]=yhl[i];yhl[i]=temp
            temp=xhr[j];xhr[j]=xhr[i];xhr[i]=temp
            temp=yhr[j];yhr[j]=yhr[i];yhr[i]=temp
            temp=xl[j];xl[j]=xl[i];xl[i]=temp
            temp=xr[j];xr[j]=xr[i];xr[i]=temp
            temp=yr[j];yr[j]=yr[i];yr[i]=temp
            temp=yl[j];yl[j]=yl[i];yl[i]=temp
            temp=rl[j];rl[j]=rl[i];rl[i]=temp
            temp=rr[j];rr[j]=rr[i];rr[i]=temp
for i in range(len(goodMatchePoints)):
     files.write(str(xl[i])+" "+str(yl[i])+"        "+str(xr[i])+" "+str(yr[i])+"      "
                + str(xhl[i])+" "+str(yhl[i])+"         "+str(xhr[i])+" "+str(yhr[i])+"    "+str(rl[i])+"\n")
files.close()
outImg = None
outImg = cv2.drawMatches(img1,cv_kpts1,img2,cv_kpts2,goodMatchePoints,
    outImg,matchColor=(0,255,0),flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)

img1_color=cv2.imread('Left.jpg')
img2_color=cv2.imread('Right.jpg')
i=0
draw_pt=[]
while i<len(xhl):
    radius=int(rl[i])
    j=i+1
    while j<len(xhl):
        if abs(xhl[j]-xhl[i])+abs(yhl[j]-yhl[i])>50:
            break
        j=j+1
    if (j-i)>=3:
        cv2.circle(img1_color,(xhl[i],yhl[i]),radius,(0,0,255),3)
        cv2.circle(img2_color,(xhr[i]-1520,yhr[i]),radius,(0,0,255),3)
        draw_pt.append([xhl[i],yhl[i],xhr[i],yhr[i]])
    i=j
cv2.imwrite("FinalMatch_Color.jpg",outImg)
final_matrix = np.zeros((1520, 3040, 3), np.uint8)

final_matrix[0:1520, 0:1520] = img1_color
final_matrix[0:1520, 1520:3040] = img2_color
for i in draw_pt:
    cv2.line(final_matrix,(i[0],i[1]),(i[2],i[3]),(0,0,255),2)
cv2.imwrite("FinalCircle_Match.jpg",final_matrix)