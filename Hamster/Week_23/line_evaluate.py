'''
Author: your name
Date: 2021-08-12 15:16:16
LastEditTime: 2021-11-08 16:29:21
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \test\test.py
'''
import cv2
import numpy as np
import math
import line_scope
import draw_result_color

# new_lines[0][0] 第一组直线的第一个点x坐标
#new_lines = line_scope.lines.reshape(-1,4)

#这个方法是用于判定模型的任意两个点之间是否有直线存在，便于进行三维重建
#new_lines houghlinesP找到的直线（用两个点来表示两点之间的直线）
#f_circle houghcircle找到的结点中心坐标
#offset 结点中心坐标+-一个常数
#angle_offset_permit 允许的角度偏差（单位是角度，不是弧度制），也就是直线之间斜率的偏差
#line_distance_permit是两直线允许的误差
#返回一个n*n的数组，数组[i][j]为1代表点ij之间存在直线

def score(value,permit):
    if (value < 0.5*permit) :return 1
    if (value < 0.8*permit) :return 0.6
    if (value <= permit): return 0.3
    return 0
def dis_score(value,permit):
    if (value < 0.3*permit) :return 1
    if (value <= permit) :return 0.6
    if (value <= 1.3*permit): return 0.3
    return 0
def max_value(a,b):
    if a>=b : return a
    return b
def line_exist(new_lines, f_circle, offset, angle_offset_permit, line_distance_permit):
    #rows, cols = (len(f_circle), len(f_circle))
    array_output = np.zeros((19,19),dtype=np.double)

    for i in range(len(f_circle)):
        for j in range(len(f_circle)):
            if i==j : continue
            #反正切角计算
            angle = math.atan2(f_circle[j][1] - f_circle[i][1], f_circle[j][0] - f_circle[i][0]) 
            for m in range(len(new_lines)):
                if (m>=50):
                    m=m
                #限定houghlinesP的直线集合在两个目标点的矩形范围内, 
                # offset 为调整量，如果两个点基本在同一垂线，那么范围应该适当扩大
                if (max(new_lines[m][0], new_lines[m][2]) > max(f_circle[i][0], f_circle[j][0]) + offset) and (max(new_lines[m][1], new_lines[m][3]) > max(f_circle[i][1], f_circle[j][1]) + offset) and\
                    (min(new_lines[m][0], new_lines[m][2]) < max(f_circle[i][0], f_circle[j][0]) - offset) and (min(new_lines[m][1], new_lines[m][3]) < min(f_circle[i][1], f_circle[j][1]) - offset):
                    continue
                else:
                    angle_houghlinesP = math.atan2(new_lines[m][3] - new_lines[m][1], new_lines[m][2] - new_lines[m][0])
                #angle_offset_permit 是允许角度偏差的最值
                angle_score=score(abs(angle - angle_houghlinesP)/math.pi*180,angle_offset_permit)
                if angle_score==0 :continue

                #通过判断两直线的距离来判定有无直线
                distance = line_line_distance(f_circle[i][0], f_circle[i][1], f_circle[j][0], f_circle[j][1], new_lines[m][0], new_lines[m][1], new_lines[m][2], new_lines[m][3], angle, angle_houghlinesP)
                distance_score=dis_score(distance,line_distance_permit)
                array_output[i][j]=max_value(array_output[i][j],distance_score*angle_score)
    return array_output


# 直线判定的标准：atan2加上两直线的距离，如果斜率相近则进行直线距判断，把其中一个点和目标区域的标准直线atan2作为斜率，计算两直线之间的距离。
#x1y1x2y2 angle1为f_circle找到的结点坐标代表的直线
def line_line_distance(x1, y1, x2, y2, x3, y3, x4, y4, angle1, angle2):  
    if (angle1 == angle2):
        result = parallel_line_line_distance(x1, y1, x2, y2, x3, y3, x4, y4, angle1)
    else:
        result = unparallel_line_line_distance(x1, y1, x2, y2, x3, y3, x4, y4, angle2)
    return result

def unparallel_line_line_distance(x1, y1, x2, y2, x3, y3, x4, y4, angle2):
    d1 = point_line_distance(x3, y3, x4, y4, x1, y1, angle2)
    d2 = point_line_distance(x3, y3, x4, y4, x2, y2, angle2)
    return max(d1, d2)

def parallel_line_line_distance(x1, y1, x2, y2, x3, y3, x4, y4, angle):
    if (angle != math.pi/2):
        k = (y2-y1)/(x2-x1)
        b1 = y1 - k*x1
        b2 = y3 - k*x3
        distance = abs(b1-b2)/math.sqrt(1 + math.pow(k, 2))
    else:
        distance = abs(x3-x1)
    return distance

def point_line_distance(x1, y1, x2, y2, x3, y3, angle1):
    if (angle1 != math.pi/2):
        if (float(x2)-float(x1)==0): return 214748
        k = (float(y2)-float(y1))/(float(x2)-float(x1))
        b = y1 - k*x1
        distance = abs(k*x3-y3+b)/math.sqrt(1+math.pow(k, 2))
    else:
        distance = abs(x3-x1)
    return distance



#print(point_line_distance(1,1,1,4,5,4,math.pi/2))
#print(parallel_line_line_distance(1,1,2,2,0,-1,1,0,math.pi/4))
#print(parallel_line_line_distance(1,1,1,4,2,1,2,4,math.pi/2))
#print(line_line_distance(0,0,4,4,0,-2.5,2.5,0,math.pi/4, math.pi/4))
#print(line_line_distance(0,0,0,4,-2.5,0,-2.5,10,math.pi/2, math.pi/2))
#print(line_line_distance(-1,-1,4,4,0,-3,4,0,math.pi/4, 0.6435))
    #np.zeros   布尔数组作为最后的输出
    #划分三档区域，最核心区域直线近似，记为1， 中间区域记为2/3, 外围区域记为1/3，左右相机加权后处理总结果
    
    
line_exist_result=line_exist(line_scope.line_scope("Left3.jpg"),draw_result_color.draw_pt,3,3,12)

line_exist_draw=cv2.imread("Left3.jpg")
for i in range(len(draw_result_color.draw_pt)):
    for j in range(len(draw_result_color.draw_pt)):
        #print(line_exist_result[i][j])
        if i==j : continue
        if line_exist_result[i][j]==0: continue
        x1=draw_result_color.draw_pt[i][0]
        y1=draw_result_color.draw_pt[i][1]
        x2=draw_result_color.draw_pt[j][0]
        y2=draw_result_color.draw_pt[j][1]
        cv2.circle(line_exist_draw,(x1,y1),draw_result_color.draw_pt[i][4],(0,0,255),2)
        cv2.circle(line_exist_draw,(x2,y2),draw_result_color.draw_pt[j][4],(0,0,255),2)
        if line_exist_result[i][j]>=0.8: 
            cv2.line(line_exist_draw,(x1,y1),(x2,y2),(0,255,100),2)
        else:
            if line_exist_result[i][j]>=0.3:
                cv2.line(line_exist_draw,(x1,y1),(x2,y2),(0,255,255),2)
            else:
                cv2.line(line_exist_draw,(x1,y1),(x2,y2),(0,0,255),2)
cv2.imwrite("line_evaluate.jpg",line_exist_draw)