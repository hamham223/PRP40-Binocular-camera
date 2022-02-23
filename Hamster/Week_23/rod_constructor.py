import mySURF
import exist_line
import kmeans
import cv2 
import numpy as np

Left_mean = kmeans.Kmean_X.cluster_centers_
Right_mean = kmeans.Kmean_Y.cluster_centers_
img1_color = mySURF.img1_color
img2_color = mySURF.img2_color
Blank_Match = kmeans.Blank

#draw the cube
line_list=[]
Font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(Left_mean)):
    #print("i = "+str(i)+",  "+str(Left_mean[i]))
    x1=int(Left_mean[i][0]);y1=Left_mean[i][1]
    cv2.putText(Blank_Match,str(i),(int(x1),int(y1)),Font,1.5,(255,255,255),2)
    for j in range(len(Left_mean)):
        if (i>=j): continue
        x2=int(Left_mean[j][0]);y2=Left_mean[j][1]
        if ((x1 == 491) & (x2==302)) | ((x1 == 302) & (x2 ==491)):
            print("here")
        if exist_line.exist_line(img1_color,x1,y1,x2,y2) | exist_line.exist_line(img1_color,x1,y1,x2,y2-5) |exist_line.exist_line(img1_color,x1,y1,x2,y2+5) | exist_line.exist_line(img1_color,x1,y1,x2-5,y2) |exist_line.exist_line(img1_color,x1,y1,x2+5,y2):
            cv2.line(Blank_Match,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
            line_list.append([i,j])
            #x1=Right_mean[i][0];y1=Right_mean[i][1]
            #x2=Right_mean[j][0];y2=Right_mean[j][1]
            #cv2.line(Blank_Match,(int(x1+1520),int(y1)),(int(x2+1520),int(y2)),(0,255,0),2)
np.save('Line_List',line_list)
print(line_list)
#for i in range(len(Right_mean)):
#    for j in range(len(Right_mean)):
#        if (i>=j): continue
#        x1=Right_mean[i][0];y1=Right_mean[i][1]
#        x2=Right_mean[j][0];y2=Right_mean[j][1]
#        if exist_line.exist_line(img2_color,x1,y1,x2,y2):
#            cv2.line(Blank_Match,(int(x1+1520),int(y1)),(int(x2+1520),int(y2)),(0,255,0),2)
#np.save('Left_mean_coord_8',Left_mean)
#np.save('Right_mean_coord_8',Right_mean)
cv2.imwrite("Blank_Match.jpg",Blank_Match)
