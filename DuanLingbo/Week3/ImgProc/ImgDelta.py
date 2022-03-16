from PIL import Image
from numpy import *
from pylab import *

Img1=array(Image.open('../Photo/ImgROF_1_Enhanced.jpg').convert('L'));
Img2=array(Image.open('../Photo/ImgROF_2_Enhanced.jpg').convert('L'));

DelImg=abs(Img1-Img2);

DelImg=DelImg*(DelImg>250);

figure(); gray(); imshow(DelImg); show();

imsave('../Photo/ImgDelta.jpg',DelImg);
