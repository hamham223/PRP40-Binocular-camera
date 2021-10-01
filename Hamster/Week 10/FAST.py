import cv2

img=cv2.imread("NaCl.jpg")
imgGray=cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
imggray=imgGray
length=len(imgGray)
width=len(imgGray[0])
for u in range(0,length):
    for v in range(0,width):
        imggray[u][v]=(img[u][v][0]*8+img[u][v][1]+img[u][v][2])/10
t=15
x=[0,1,2,3,3,3,2,1,0,-1,-2,-3,-3,-3,-2,-1]
y=[3,3,2,1,0,-1,-2,-3,-3,-3,-2,-1,0,1,2,3]

def mark(x0,y0):
    for i in range(0,15):
        x1=x0+x[i]
        y1=y0+y[i]
        img[x1][y1]=[0 ,255, 0]
    #img[x0][y0]=[0,255,0]

for u in range(3,length-3):
    for v in range(3,width-3):
        gray=imggray[u][v]
        num=0
        boo=0
        for k in [0,4,8,12]:
            u1=u+x[k]
            v1=v+y[k]
            if abs(int(imggray[u1][v1]) - int(imggray[u][v])) >= t : num=num+1
        if num<=2 :continue
        num=0
        for k in range(0,15):
            u1=u+x[k]
            v1=v+y[k]
            if abs(int(imggray[u1][v1]) - int(imggray[u][v])) >= t : num=num+1
            else: num=0
            if num>=9: boo=1
        if boo == 1 : mark(u,v)
cv2.imshow("gray",img)
cv2.waitKey(10000)
cv2.destroyAllWindows()

