import cv2
import numpy as np

Draw_test_circle=np.zeros((100,100, 3), np.uint8)
cv2.circle(Draw_test_circle,(50,50),10,(99,12,50),-1,8)

cv2.imshow("Draw_test_circle",Draw_test_circle)
cv2.waitKey(5000)
cv2.destroyAllWindows()
print(Draw_test_circle[45][45])
cv2.imwrite("test_draw_circle.jpg",Draw_test_circle)

img=cv2.imread("test_draw_circle.jpg")
print(img[45][45])