import numpy
import cv2
from numpy.lib.shape_base import expand_dims

R=numpy.array([ 0.99763786 , 0.00326705 , 0.06861506],
[-0.00318983,  0.99999415, -0.00123497],[-0.06861869 , 0.00101318,  0.99764245])
T=numpy.array([ 0.16780832],[-0.01496177],[-0.03598987])

Camera_Left=numpy.array([1.48328735e+03, 0.00000000e+00, 7.34012939e+02],
 [0.00000000e+00, 1.48171814e+03, 8.59885951e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00])

RT=numpy.array([ 0.99763786 , 0.00326705 , 0.06861506,0.16780832 ],
[-0.00318983,  0.99999415, -0.00123497,-0.01496177],[-0.06861869 , 0.00101318,  0.99764245,-0.03598987],
[0,0,0,1])
P=numpy.array()
img=cv2.imread("try.jpg")
l1=len(img)
l2=len(img[0])
for u in 1:l1
    for v in 1:l2
        P=numpy.matmul(Camera_Left,RT)
    break