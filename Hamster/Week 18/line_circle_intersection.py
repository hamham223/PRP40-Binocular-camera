import line_scope
import draw_result_color
import numpy as np
import math

def dis(x,y,cx,cy,r):
    x=float(x)
    y=float(y)
    cx=float(cx)
    cy=float(cy)
    r=float(r)
    distance=abs(math.sqrt((x-cx)**2+(y-cy)**2)-r)
    return (distance<18)

Line_left=line_scope.line_scope("Left3.jpg")
Line_right=line_scope.line_scope("Right3.jpg")

Line_match_left=np.zeros((400,2),dtype=np.uint8)
Line_match_right=np.zeros((400,2),dtype=np.uint8)
for j in Line_match_right:
    j[0]=-1
    j[1]=-1    
for j in Line_match_left:
    j[0]=-1
    j[1]=-1 


count_i=0
for i in draw_result_color.draw_pt:
    circle_x=i[0]
    circle_y=i[1]
    radii=i[4]
    count_j=0
    for j in Line_left:
        if dis(j[0][0],j[0][1],circle_x,circle_y,radii):
            if Line_match_left[count_j][0]!=-1 :
                Line_match_left[count_j][1]=count_i
                continue
            Line_match_left[count_j][0]=count_i
        count_j=count_j+1
    count_j=0
    for j in Line_right:
        if dis(j[0][2],j[0][3],circle_x,circle_y,radii):
            if Line_match_right[count_j][0]!=-1 :
                Line_match_right[count_j][1]=count_i
                continue
            Line_match_right[count_j][0]=count_i
        count_j=count_j+1
    count_i=count_i+1

line_circle_file=open("line_circle_match.txt",'w')
line_circle_file.write("Left Line Position         Match_circle:\n")
for j in range(0,len(Line_left)):
    if Line_match_left[j][0]==-1:
        continue
    write_str=str(Line_left[j][0][0])+"    "+str(Line_left[j][0][1])
    write_str=write_str+"       "+str(Line_match_left[j][0])+"    "+str(Line_match_left[j][1])
    line_circle_file.write(write_str+"\n")
line_circle_file.write("\n\n\nRight Line Position        Match_circle:\n")
for j in range(0,len(Line_right)):
    if Line_match_right[j][0]==-1:
        continue
    write_str=str(Line_right[j][0][0])+"    "+str(Line_right[j][0][1])
    write_str=write_str+"       "+str(Line_match_right[j][0])+"    "+str(Line_match_right[j][1])
    line_circle_file.write(write_str+"\n")
line_circle_file.close()