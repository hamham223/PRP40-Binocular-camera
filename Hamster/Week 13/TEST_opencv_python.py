import cv2
import numpy as np

img=np.zeros((300,300,3),dtype=np.uint8)
img[:,0:100,0]=255
img[:,100:200,1]=255
img[:,200:300,2]=255

print("img=\n",img)

cv2.imshow("AAA",img)
cv2.waitKey()
cv2.destroyAllWindows()