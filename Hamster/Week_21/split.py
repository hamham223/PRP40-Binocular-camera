import cv2
for i in range(1,3):
    #str_="Origin_"+str(i)+".jpg"
    #print(str_)
    img=cv2.imread("Origin_"+str(i)+".jpg")
    
    i1=img[0:1520,0:1520]
    i2=img[0:1520,1520:3040]
    cv2.imwrite("Left_"+str(i)+".jpg",i1)
    cv2.imwrite("Right_"+str(i)+".jpg",i2)
    print(i1.shape)
    print(i2.shape)