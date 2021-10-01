import cv2 as cv
import numpy as np
import glob

# Read images and crop into left and right
img_original = glob.glob('./img_original/*.jpg')
count = 1
for jpg_o in img_original:
    img = cv.imread(jpg_o)
    width = int(img.shape[1])
    height = int(img.shape[0])
    img_L = img[0:height, 0:int(width / 2)]
    img_R = img[0:height, int(width / 2):width]
    # width_new_L = int(img_L.shape[1]*0.2)
    # height_new_L = int(img_L.shape[0]*0.2)
    # width_new_R = int(img_R.shape[1]*0.2)
    # height_new_R = int(img_R.shape[0]*0.2)
    # img_L = cv.resize(img_L, (width_new_L, height_new_L), interpolation = cv.INTER_AREA)
    # img_R = cv.resize(img_R, (width_new_R, height_new_R), interpolation = cv.INTER_AREA)
    resultL = './imgL/' + str(count) + '.jpg'
    resultR = './imgR/' + str(count) + '.jpg'
    cv.imwrite(resultL, img_L)
    cv.imwrite(resultR, img_R)
    count = count + 1
    
frameSize = (img_L.shape[0], img_L.shape[1])
# Find checkerboard patterns
CHECKERBOARD = (5, 7)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints = []
imgpointsL = []
imgpointsR = []

objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

count = 0
imagesLeft = glob.glob('imgL/*.jpg')
imagesRight = glob.glob('imgR/*.jpg')
for imLeft, imRight in zip(imagesLeft, imagesRight):
    imgL = cv.imread(imLeft)
    imgR = cv.imread(imRight)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    retL, cornersL = cv.findChessboardCorners(grayL, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH+
    	cv.CALIB_CB_FAST_CHECK+cv.CALIB_CB_NORMALIZE_IMAGE)
    retR, cornersR = cv.findChessboardCorners(grayR, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH+
    	cv.CALIB_CB_FAST_CHECK+cv.CALIB_CB_NORMALIZE_IMAGE)
    
    if retL == True and retL == True:
        objpoints.append(objp)
        cornersL = cv.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        cornersR = cv.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)
        cv.drawChessboardCorners(imgL, CHECKERBOARD, cornersL, retL)
        cv.drawChessboardCorners(imgR, CHECKERBOARD, cornersR, retR)
        result_file_L = './results/result' + str(count) + 'L.png'
        result_file_R = './results/result' + str(count) + 'R.png'
        cv.imwrite(result_file_L, imgL)
        cv.imwrite(result_file_R, imgR)
    
    count = count + 1

# Calibration
retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

#Stereo vision calibration
flags = 0
flags |= cv.CALIB_FIX_INTRINSIC
criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, 
    imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

print("Camera Matrix Left:")
print(newCameraMatrixL)
print("Camera Matrix Right:")
print(newCameraMatrixR)
print("distL:")
print(distL)
print("distR:")
print(distR)
print("Rotation:")
print(rot)
print("Transposition:")
print(trans)
