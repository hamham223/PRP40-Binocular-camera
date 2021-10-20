import line_scope
import draw_result_color
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
def dis(x,y,cx,cy,r):
    x=float(x)
    y=float(y)
    cx=float(cx)
    cy=float(cy)
    r=float(r)
    distance=abs(math.sqrt((x-cx)**2+(y-cy)**2)-r)
    return (distance<117)

Line_left=line_scope.line_scope("Left3.jpg")
Line_right=line_scope.line_scope("Right3.jpg")

Line_match_left=np.zeros((400,3),dtype=np.uint8)
Line_match_right=np.zeros((400,3),dtype=np.uint8)


count_i=0
for i in draw_result_color.draw_pt:
    circle_x=i[0]
    circle_y=i[1]
    radii=i[4]
    count_j=0
    for j in Line_left:
        if dis(j[0][0],j[0][1],circle_x,circle_y,radii):
            if (Line_match_left[count_j][2]==2) :
                continue
            ccc=Line_match_left[count_j][2]
            Line_match_left[count_j][ccc]=count_i
            Line_match_left[count_j][2]+=1
        count_j=count_j+1
    count_j=0
    circle_x=i[2]-1520
    circle_y=i[3]
    for j in Line_right:
        if dis(j[0][2],j[0][3],circle_x,circle_y,radii):
            if (Line_match_right[count_j][2]==2) :
                continue
            ccc=Line_match_right[count_j][2]
            Line_match_right[count_j][ccc]=count_i
            Line_match_right[count_j][2]+=1
        count_j=count_j+1
    count_i=count_i+1

line_circle_left_img=np.zeros((1520,1520,3),np.uint8)
line_circle_file=open("line_circle_match.txt",'w')
line_circle_file.write("Left Line Position                Match_circle:\n")
for j in range(0,len(Line_left)):
    if Line_match_left[j][2]<=1:
        continue
    write_str=str(Line_left[j][0][0])+"   "+str(Line_left[j][0][1])+"  "+str(Line_left[j][0][2])+"  "+str(Line_left[j][0][3])
    write_str=write_str+"       "+str(Line_match_left[j][0])+"    "+str(Line_match_left[j][1])+"     "+str(Line_match_left[j][2])
    if Line_match_left[j][2]>=1:
        circle_x=draw_result_color.draw_pt[Line_match_left[j][0]][0]
        circle_y=draw_result_color.draw_pt[Line_match_left[j][0]][1]
        radii=draw_result_color.draw_pt[Line_match_left[j][0]][4]
        cv2.circle(line_circle_left_img,(circle_x,circle_y),radii,(0,0,255),-1)
        cv2.line(line_circle_left_img,(Line_left[j][0][0],Line_left[j][0][1]),(Line_left[j][0][2],Line_left[j][0][3]),(0,255,0),2)
        
        circle_x=draw_result_color.draw_pt[Line_match_left[j][0]][2]
        circle_y=draw_result_color.draw_pt[Line_match_left[j][0]][3]
        radii=draw_result_color.draw_pt[Line_match_left[j][0]][4]
        cv2.circle(line_circle_left_img,(circle_x,circle_y),radii,(0,0,255),-1)
    line_circle_file.write(write_str+"\n")
line_circle_file.write("\n\n\nRight Line Position        Match_circle:\n")
for j in range(0,len(Line_right)):
    if Line_match_right[j][2]<=1:
        continue
    write_str=str(Line_right[j][0][0])+"    "+str(Line_right[j][0][1])
    write_str=write_str+"       "+str(Line_match_right[j][0])+"    "+str(Line_match_right[j][1])+"    "+str(Line_match_right[j][2])
    line_circle_file.write(write_str+"\n")
line_circle_file.close()

plt.imshow(line_circle_left_img),plt.show()
cv2.imwrite("Line_circle_left.jpg",line_circle_left_img)
