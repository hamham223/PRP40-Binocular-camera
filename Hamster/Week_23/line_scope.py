from cmath import pi
import cv2
import numpy as np
import math

def line_scope(file_name):
    img = cv2.imread(file_name)

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
            if y2==1150 :
                print(x1,y1,x2,y2)
                cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),2)
                break
            cv2.line(line_image,(x1,y1),(x2,y2),(255,255,0),2)
            
    cv2.imwrite("line_"+file_name,line_image)
    return_line=[]
    angle=[]
    dis=[]
    line_file=open("line_scope_"+file_name+".txt",'w')
    for i in lines:
        return_line.append(i[0])
        x1=i[0][0];y1=i[0][1];x2=i[0][2];y2=i[0][3]
        angle.append(math.atan2(y2-y1,x2-x1)/pi*180)
        dis.append(math.sqrt((y2-y1)**2+(x2-x1)**2))
        line_file.write(str(i[0])+'\n')
    line_file.close()
    return return_line,angle,dis

# Draw the lines on the  image
#lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
line,angle,dis=line_scope("Left_6.jpg")
line_scope("Right_6.jpg")

_angle=open("angle.txt",'w')
for i in angle:
    _angle.write(str(i)+"\n")
_angle.write("\n\n")
for i in dis:
    _angle.write(str(i)+"\n")