import cv2

img=cv2.imread("New.jpg")

i1=img[0:1520,0:1520]
i2=img[0:1520,1520:3040]
cv2.imwrite("Left3.jpg",i1)
cv2.imwrite("Right3.jpg",i2)
print(i1.shape)
print(i2.shape)