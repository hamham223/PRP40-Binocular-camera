import cv2
import matplotlib.pyplot as plt
import calc_median_color
import numpy as np
import exist_line
import if_blue
import mean_coord
import exist_line

_index=9;index=str(_index)
img = cv2.imread('origin/big ('+index+').jpg')
img1 = cv2.imread('Left_'+index+'.jpg',cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Right_'+index+'.jpg',cv2.IMREAD_GRAYSCALE)
img1_color = cv2.imread('Left_'+index+'.jpg')
img2_color = cv2.imread('Right_'+index+'.jpg')
#create a SURF object
#threshold,feature,otcave,dimension,upright
surf = cv2.xfeatures2d.SURF_create(0,8,4,0,0)
#detect
k1,descriptor1 = surf.detectAndCompute(img1,None)
k2,descriptor2 = surf.detectAndCompute(img2,None)

matcher = cv2.FlannBasedMatcher()
matchePoints = matcher.match(descriptor1,descriptor2)

#提取强匹配特征点
minMatch = 1
maxMatch = 0
for i in range(len(matchePoints)):
    if minMatch > matchePoints[i].distance:
        minMatch = matchePoints[i].distance
    if maxMatch < matchePoints[i].distance:
        maxMatch = matchePoints[i].distance
#print('最佳匹配值是:',minMatch)
#print('最差匹配值是:',maxMatch)
goodMatchePoints = []
Blank_Match=np.zeros((1520, 3040, 3), np.uint8)
mean_color_file=open("mean_color.txt",'w')
for i in range(len(matchePoints)):
    if matchePoints[i].distance < minMatch + (maxMatch-minMatch)/16+100:
        left_id=matchePoints[i].queryIdx
        right_id=matchePoints[i].trainIdx
        xl=int(k1[left_id].pt[0])
        yl=int(k1[left_id].pt[1])
        xr=int(k2[right_id].pt[0]+1520)
        yr=int(k2[right_id].pt[1])
        #print(xl,yl,xr-1520,yr,img1_color[yl][xl],img2_color[yr][xr-1520])
        if abs(float(yr-yl)/float(xr-xl))<0.03:
            if (if_blue.if_blue(img1_color[yl][xl])) & (if_blue.if_blue(img2_color[yr][xr-1520])):
                goodMatchePoints.append(matchePoints[i])
                cv2.circle(Blank_Match,(xl,yl),3,(0,255,0),-1)
                cv2.circle(Blank_Match,(xr,yr),3,(0,255,0),-1)
        #print(img1_color[xl][yl],img2_color[xr-1520][yr])

#get mean coordinates
[Left,Right]=mean_coord.get_coord(goodMatchePoints,k1,k2)
left_right=open("left_right.txt",'w')
left_right.write("Left:\n")
for i in Left: left_right.write(str(len(i))+"\n")
left_right.write("Right\n")
for i in Right: left_right.write(str(len(i))+"\n")
left_right.close()
Left_mean=[];Right_mean=[]
for j in Left:
    count_x=0;count_y=0;count=0
    for k in j:
        count+=1;count_x+=k[0];count_y+=k[1]
    temp_x=int(count_x/count);temp_y=int(count_y/count)
    Left_mean.append([temp_x,temp_y])
    cv2.circle(Blank_Match,(temp_x,temp_y),10,(255,0,255),2)
for j in Right:
    count_x=0;count_y=0;count=0
    for k in j:
        count+=1;count_x+=k[0];count_y+=k[1]
    temp_x=int(count_x/count);temp_y=int(count_y/count)
    Right_mean.append([temp_x,temp_y])
    cv2.circle(Blank_Match,(temp_x+1520,temp_y),10,(255,0,255),2)
for j in range(min(len(Left_mean),len(Right_mean))):
    print(Left_mean[j],Right_mean[j])
    xl=Left_mean[j][0];yl=Left_mean[j][1]
    xr=Right_mean[j][0];yr=Right_mean[j][1]
    cv2.line(Blank_Match,(int(xl),int(yl)),(int(xr+1520),int(yr)),(255,255,0),2)


#draw the cube
for i in range(len(Left_mean)):
    for j in range(len(Left_mean)):
        if (i>=j): continue
        x1=Left_mean[i][0];y1=Left_mean[i][1]
        x2=Left_mean[j][0];y2=Left_mean[j][1]
        if exist_line.exist_line(img1_color,x1,y1,x2,y2):
            cv2.line(Blank_Match,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
for i in range(len(Right_mean)):
    for j in range(len(Right_mean)):
        if (i>=j): continue
        x1=Right_mean[i][0];y1=Right_mean[i][1]
        x2=Right_mean[j][0];y2=Right_mean[j][1]
        if exist_line.exist_line(img2_color,x1,y1,x2,y2):
            cv2.line(Blank_Match,(int(x1+1520),int(y1)),(int(x2+1520),int(y2)),(0,255,0),2)



#imwrite
outImg = None
outImg = cv2.drawMatches(img1_color,k1,img2_color,
    k2,goodMatchePoints,outImg,
    matchColor=(0,255,0),flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
cv2.imwrite("Match.jpg",outImg)
cv2.imwrite("Blank_Match.jpg",Blank_Match)
mean_color_file.close()
plt.imshow(Blank_Match),plt.show()