import math
import cv2
from matplotlib.pyplot import xcorr
import HoughLineDetect
import draw_result_color

def drawline(lA,lB,lC):
    y_axis=int(-lC/lB)
    

def dis(pt_x,pt_y,_A,_B,_C):
    numer=abs(_A*pt_x+_B*pt_y+_C)
    dino=math.sqrt(_A*_A+_B*_B)
    return numer/dino

count=len(HoughLineDetect.lista)
line=[]
for i in draw_result_color.draw_pt:
    p_x=i[0]
    p_y=i[1]
    minDis=6080
    m_A=1
    m_B=1
    m_C=1 #record the corresponding ABC
    for j in range(0,count):
        lA=HoughLineDetect.lista[j]
        lB=HoughLineDetect.listb[j]
        lC=HoughLineDetect.listc[j]
        if dis(p_x,p_y,lA,lB,lC)<minDis:
            minDis=dis(p_x,p_y,lA,lB,lC)
            m_A=lA
            m_B=lB
            m_C=lC
    print(minDis)
    line.append([m_A,m_B,m_C,minDis])
    
img=cv2.imread("Left3.jpg")
for draw_line in line:
    lA=draw_line[0]
    lB=draw_line[1]
    lC=draw_line[2]
    cv2.line(img, (0, int(-lC/lB)), (400, int(-(lC+lA*400)/lB)), (0, 0, 255), 2)
    print(int(lA),int(lB),int(lC))
cv2.imwrite("HoughLine_Circle.jpg",img)