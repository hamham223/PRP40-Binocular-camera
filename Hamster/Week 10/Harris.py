import cv2
import numpy as np
import operator
import copy
def findCorners(img, window_size, k, thresh):
    """
    Finds and returns list of corners and new image with corners drawn
    :param img: The original image
    :param window_size: The size (side length) of the sliding window
    :param k: Harris corner constant. Usually 0.04 - 0.06
    :param thresh: The threshold above which a corner is counted
    :return:
    """
    #Find x and y derivatives
    dy, dx = np.gradient(img)
    Ixx = dx**2
    Ixy = dy*dx
    Iyy = dy**2
    height = img.shape[0]
    width = img.shape[1]

    cornerList = []
    newImg = img.copy()
    color_img = cv2.cvtColor(newImg, cv2.COLOR_GRAY2RGB)
    offset = int(window_size/2)

    #Loop through image and find our corners
    print("Finding Corners...")
    for y in range(offset, height-offset):
        for x in range(offset, width-offset):
            #Calculate sum of squares
            windowIxx = Ixx[y-offset:y+offset+1, x-offset:x+offset+1]
            windowIxy = Ixy[y-offset:y+offset+1, x-offset:x+offset+1]
            windowIyy = Iyy[y-offset:y+offset+1, x-offset:x+offset+1]
            Sxx = windowIxx.sum()
            Sxy = windowIxy.sum()
            Syy = windowIyy.sum()

            #Find determinant and trace, use to get corner response
            det = (Sxx * Syy) - (Sxy**2)
            trace = Sxx + Syy
            r = det - k*(trace**2)

            #If corner response is over threshold, color the point and add to corner list
            if r > thresh:
                #print( x, y, r)
                cornerList.append([x, y, r])
                mark[y][x]=1
                #color_img.itemset((y, x, 0), 255)
                #color_img.itemset((y, x, 1), 0)
                #color_img.itemset((y, x, 2), 0)
    return color_img, cornerList

#def main():


window_size = 5
k = 0.06
thresh = 1100


img=cv2.imread("ppt.png")
imggray=cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
mark=copy.copy(imggray)
for i in range(0,len(mark)):
    for j in range(0,len(mark[0])):
        mark[i][j]=0
#print ("Shape: " + str(img.shape))
#print ("Size: " + str(img.size))
#print ("Type: " + str(img.dtype))
#print ("Printing Original Image...")
finalImg, cornerList = findCorners(imggray, int(window_size), float(k), int(thresh))

dx=[1,0,-1,0]
dy=[0,1,0,-1]
judge=copy.copy(mark)
outfile = open('tails.txt', 'w')
for i in range(0,len(cornerList)):
    x=cornerList[i][0]
    y=cornerList[i][1]
    if mark[y][x]==1:
        head=-1
        tail=0
        queue=[]
        queue.append([x,y])
        while (head<tail):
            head=head+1
            hx=queue[head][0]
            hy=queue[head][1]
            for k in range(0,3):
                tx=hx+dx[k]
                ty=hy+dy[k]
                if mark[ty][tx]==1 : 
                    mark[ty][tx]=0
                    tail=tail+1
                    queue.append([tx,ty])
        if tail < 1:
            for j in range(0,len(queue)):
                judge[queue[j][1]][queue[j][0]]=0
        else: 
            outfile.write(str(tail)+'\n')
for i in range(0,len(cornerList)):
    x=cornerList[i][0]
    y=cornerList[i][1]
    if (judge[y][x]==1):
        img[y][x]=[0,255,0]
cv2.imwrite("finalimage.png", img)
cv2.imshow("finalimg",img)
cv2.waitKey()
cv2.destroyAllWindows()
outfile.close()
 #Write top 100 corners to file
#cornerList.sort(key=operator.itemgetter(2))
#outfile = open('corners.txt', 'w')
#for i in range(100):
#    outfile.write(str(cornerList[i][0]) + ' ' + str(cornerList[i][1]) + ' ' + str(cornerList[i][2]) + '\n')
#outfile.close()