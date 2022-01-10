import cv2
import surf_match
import calc_median_color
import numpy as np


img1_color=cv2.imread('Left_1.jpg')
img2_color=cv2.imread('Right_1.jpg')
i=0
draw_pt=[]
color_pt=[]
while i<len(surf_match.xhl):
    radius=int(surf_match.rl[i])
    j=i+1
    while j<len(surf_match.xhl):
        if int(abs(int(surf_match.xhl[j])-int(surf_match.xhl[i])))+int(abs(int(surf_match.yhl[j])-int(surf_match.yhl[i])))>50:
            break
        j=j+1
    if (j-i)<2:
        i=j
        continue
    m_color_1=calc_median_color.calc_median_color(img1_color,surf_match.yhl[i],surf_match.xhl[i],radius)
    m_color_2=calc_median_color.calc_median_color(img2_color,surf_match.yhr[i],surf_match.xhr[i]-1520,radius)
    #if ((m_color_1[0]<=73)|(m_color_1[0]>=120)&(m_color_1[0]<=185))&(m_color_2[0]<=200):
    if (((m_color_1[1]>=180) & (m_color_2[1]>=160)) & (abs(m_color_2[0]-m_color_1[0])<=50)):
        cv2.circle(img1_color,(surf_match.xhl[i],surf_match.yhl[i]),radius,(0,0,255),3)
        cv2.circle(img2_color,(surf_match.xhr[i]-1520,surf_match.yhr[i]),radius,(0,0,255),3)
        draw_pt.append([surf_match.xhl[i],surf_match.yhl[i],surf_match.xhr[i],surf_match.yhr[i],radius])
        color_pt.append([m_color_1,m_color_2])
    i=j

final_matrix = np.zeros((1520, 3040, 3), np.uint8)

final_matrix[0:1520, 0:1520] = img1_color
final_matrix[0:1520, 1520:3040] = img2_color


f_circle=open("circle_match.txt",'w')
f_circle.write("Left             Right             Radius              \n")
m_color=open("m_color.txt",'w')
m_color.write("Left Mean color    Right Mean color    Position\n")

draw_cirlces = np.zeros((1520, 3040, 3), np.uint8)
count_i=0
for i in draw_pt:
    cv2.line(final_matrix,(i[0],i[1]),(i[2],i[3]),(0,0,255),2)
    f_circle.write(str(i[0])+"  "+str(i[1])+"       "+str(i[2])+"  "+str(i[3])+"      "+str(i[4])+"      \n")
    m_color.write(str(color_pt[count_i][0])+"        "+str(color_pt[count_i][1])+"         "+str(i)+"\n")
    cv2.circle(draw_cirlces,(i[0],i[1]),i[4],color_pt[count_i][0],-1,8)
    cv2.circle(draw_cirlces,(i[2],i[3]),i[4],color_pt[count_i][1],-1,8)
    count_i=count_i+1
f_circle.close()

cv2.imwrite("Draw_Circles.jpg",draw_cirlces)
cv2.imwrite("FinalCircle_Match.jpg",final_matrix)

m_color.close()