import cv2
import queue
import numpy as np
import matplotlib.pyplot as plt

dx=[1,0,-1,0];dy=[0,1,0,-1]
def if_orange(c,c1):
    if (int(c1[2]<170)): return False
    if (int(c1[0]>=50)): return False
    diff=abs(int(c[2])-int(c1[2]))#+abs(int(c[0])-int(c1[0]))#+abs(int(c[2])-int(c1[2]))
    thereshold=8
    return (diff<=thereshold)

img=cv2.imread("Left_1.jpg")
img_mark=cv2.imread("Left_1.jpg")
img_exist=np.zeros((1520,1520),dtype=bool)
x0=553 ; y0=610

pt_list=queue.Queue(-1)
pt_list.put([x0,y0])
img_exist[x0,y0]=True
img_mark=cv2.circle(img_mark,(y0,x0),1,(0,255,0),1)
mean_color=np.zeros(3,dtype=np.uint64)
count_mean_color=0
outfile=open("test.txt",'w')
while (not pt_list.empty()):
    [x,y]=pt_list.get()
    c=img[x][y]
    for i in range(0,4):
        x1=x+dx[i];y1=y+dy[i]
        if (x1>=1520 | y1>=1520 | x1<0 | y1<0): continue
        c1=img[x1][y1]
        if (img_exist[x1][y1]==False) & (if_orange(c,c1)):
            pt_list.put([x1,y1])
            img_exist[x1][y1]=True
            img_mark=cv2.circle(img_mark,(y1,x1),1,(0,255,0),1)
            mean_color[0]+=c[0];mean_color[1]+=c[1];mean_color[2]+=c[2];count_mean_color+=1
            outfile.write(str(x1)+"   "+str(y1)+"\n")
outfile.close()
for x in range(0,3): mean_color[x]=int(mean_color[x]/count_mean_color)
print(mean_color)
cv2.imwrite("mark_result.jpg",img_mark)
plt.imshow(img_mark),plt.show()
