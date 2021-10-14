'''
Author: your name
Date: 2021-09-03 09:10:43
LastEditTime: 2021-10-13 16:01:36
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \test\Hough_Line_Detect_2.py
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

src = cv2.imread('Left3.jpg')
#src = cv2.resize(src,(800,800)) #图片做缩放适应性处理
srcBlur = cv2.GaussianBlur(src, (3, 3), 0) #高斯平滑
gray = cv2.cvtColor(srcBlur, cv2.COLOR_BGR2GRAY) #高斯平滑后的图像转为灰度图
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

lista = []
listb = []
listc = []
threshold = 95
 
lines = cv2.HoughLines(edges, 1, np.pi/180, threshold) #得到所有的在threshold里的霍夫直线
img = src.copy() 
for line in lines:
    # rho = line[0][0]
    # theta = line[0][1]
    flag = 0
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)        
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    if (x2 != x1):
        k = (y2 - y1)/(x2 - x1)
        b = y2 - k * x2
        lista.append(round(k,3))
        listc.append(round(b,3))
        listb.append(-1)
    else: 
        lista.append(1)
        listc.append(round(-x1,3))
        listb.append(0)

    if (len(lista)>1):
        for i in range(0, len(lista)-1):
            if ((k - lista[i] <= 1.5) and (b- listc[i] <= 30)):
                lista.pop()
                listb.pop()
                listc.pop()
                flag = 1
                break
            else:
                continue
    if (flag == 0):
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2) #draw lines based on the original image       


cv2.imwrite("Houghline.jpg",img)
plt.imshow(img),plt.show()

