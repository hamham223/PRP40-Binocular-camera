from matplotlib import pyplot as plt
import cv2

l=cv2.imread("line_Left3.jpg")
r=cv2.imread("Right3.jpg")

plt.imshow(l),plt.show()