import cv2
import pick_surf_circle
import mySURF
import find_houghcircle

matcher = cv2.FlannBasedMatcher()
matchePoints = matcher.match(pick_surf_circle.d1,pick_surf_circle.d2)

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
files=open("match_result_1.txt",'w')
files.write("x_L "+"y_L        x_R y_R      "
                + " H_x_L H_y_L      H_x_R H_y_R    R "+"\n")
xl=[];yl=[];xr=[];yr=[];xhl=[];yhl=[];xhr=[];yhr=[];rl=[];rr=[]
for i in range(len(matchePoints)):
    if matchePoints[i].distance < minMatch + (maxMatch-minMatch):
        left_id=matchePoints[i].queryIdx
        right_id=matchePoints[i].trainIdx
        xl_temp=mySURF.k1[pick_surf_circle.key1[left_id]].pt[0]
        yl_temp=mySURF.k1[pick_surf_circle.key1[left_id]].pt[1]
        xr_temp=mySURF.k2[pick_surf_circle.key2[right_id]].pt[0]+1520
        yr_temp=mySURF.k2[pick_surf_circle.key2[right_id]].pt[1]
        if abs(float(yr_temp-yl_temp)/float(xr_temp-xl_temp))<0.04:
            
            xhl_temp,yhl_temp,rl_temp=find_houghcircle.findcircle(xl_temp,yl_temp,find_houghcircle.count1,find_houghcircle.circles1)
            xhr_temp,yhr_temp,rr_temp=find_houghcircle.findcircle(xr_temp-1520,yr_temp,find_houghcircle.count2,find_houghcircle.circles2)
            xhr_temp=xhr_temp+1520
            if abs(float(yhr_temp)-float(yhl_temp))/abs(float(xhr_temp)-float(xhl_temp))<0.02:
                goodMatchePoints.append(matchePoints[i])
                xl.append(int(xl_temp));yl.append(int(yl_temp))
                xr.append(int(xr_temp));yr.append(int(yr_temp))
                xhl.append(int(xhl_temp));yhl.append(int(yhl_temp))
                xhr.append(int(xhr_temp));yhr.append(int(yhr_temp))
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

#draw surf match result regarding to the hough circles
outImg = None
outImg = cv2.drawMatches(mySURF.img1,pick_surf_circle.cv_kpts1,mySURF.img2,
    pick_surf_circle.cv_kpts2,goodMatchePoints,outImg,
    matchColor=(0,255,0),flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
cv2.imwrite("SurfMatch_Circle.jpg",outImg)
