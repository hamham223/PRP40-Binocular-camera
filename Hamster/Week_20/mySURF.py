import cv2

img1 = cv2.imread('Left_5.jpg',cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Right_5.jpg',cv2.IMREAD_GRAYSCALE)
#create a SURF object
#threshold,feature,otcave,dimension,upright
surf = cv2.xfeatures2d.SURF_create(20,16,4,0,0)
#detect
k1,descriptor1 = surf.detectAndCompute(img1,None)
k2,descriptor2 = surf.detectAndCompute(img2,None)
    