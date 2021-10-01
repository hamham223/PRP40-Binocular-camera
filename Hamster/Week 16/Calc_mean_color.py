import cv2
import numpy as np
import math

def calc_median_color(img,x_0,y_0,r):
    count=0;color=np.zeros((3,),dtype=int)
    for i_ in range(x_0-r,x_0+r):
        for j_ in range(y_0-r,y_0+r):
            dis=math.sqrt(float((i_-x_0)**2+(j_-y_0)**2))
            if dis<=r:
                count=count+1
                color[0]=color[0]+int(img[i_,j_,0])
                color[1]=color[1]+int(img[i_,j_,1])
                color[2]=color[2]+int(img[i_,j_,2])
    color[0]=np.uint8(color[0]/count)
    color[1]=np.uint8(color[1]/count)
    color[2]=np.uint8(color[2]/count)
    return tuple([int(x) for x in color])

def main():
    hamster=cv2.imread("Hamster.jpg")
    mid_hamster=np.zeros((426,640,3),np.uint8)
    for i in range(0,25):
        for j in range(0,40):
            m_color_1=calc_median_color(hamster,15*(i+1),15*(j+1),5)
            cv2.circle(mid_hamster,(15*(j+1),15*(i+1)),5,m_color_1,-1,8)
    cv2.imwrite("Mid_Hamster.jpg",mid_hamster)
    print(hamster.shape)
main()