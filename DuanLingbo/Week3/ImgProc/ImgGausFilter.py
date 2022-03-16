# 高斯模糊
from PIL import Image
from numpy import *
from scipy.ndimage import filters
from pylab import *

Img=array(Image.open("../Photo/1.jpg"));
NewImg=zeros(Img.shape);
for i in range(3):
    NewImg[:,:,i]=filters.gaussian_filter(Img[:,:,i],5);
NewImg=array(NewImg,'uint8');
imshow(NewImg);
show();

imsave("../Photo/ImgGausFilter_1.jpg",NewImg);

