'''
Author: your name
Date: 2021-10-13 13:49:32
LastEditTime: 2021-10-13 14:14:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \test\test2.py
'''

import cv2
import numpy as np
import math

sizex = 800
sizey = 800
img = cv2.imread('Left3.jpg')
img = cv2.resize(img,(sizex,sizey)) 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),2)
cv2.imshow('drawlines', line_image)
cv2.waitKey(0)
# Draw the lines on the  image
#lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)