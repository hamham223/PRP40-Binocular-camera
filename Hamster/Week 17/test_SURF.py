import cv2
import matplotlib.pyplot as plt
#read image
#img1 = cv2.imread('hamster1.jpg',cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('hamster2.jpg',cv2.IMREAD_GRAYSCALE)
#img1 = cv2.resize(img1,(261,242)) #resize to the same

# Create SURF object. You can specify params here or later.
# Here I set Hessian Threshold to 400
surf = cv2.xfeatures2d.SURF_create(40,6,4,1,0)
# Find keypoints and descriptors directly
kp, des = surf.detectAndCompute(img2,None)
img2 = cv2.drawKeypoints(img2,kp,None,(255,0,0),4)
plt.imshow(img2),plt.show()