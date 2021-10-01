import cv2

img1=cv2.imread("Left3.jpg")
img2=cv2.imread("Right3.jpg")
i1=cv2.GaussianBlur(img1,(5,5),0,0)
i2=cv2.GaussianBlur(img2,(5,5),0,0)
cv2.imwrite("Left4.jpg",i1)
cv2.imwrite("Right4.jpg",i2) 