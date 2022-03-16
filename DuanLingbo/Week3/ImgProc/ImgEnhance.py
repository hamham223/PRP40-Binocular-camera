import ImgTools
import os
from PIL import Image
from pylab import *
Img=array(Image.open("../Photo/ImgROF_1.jpg").convert('L'));
NewImg,cdf=ImgTools.HistEq(Img);
figure(); imshow(NewImg); title('NewImg');
figure(); imshow(Img); title('Img');
show();

imsave("../Photo/ImgROF_1_Enhanced.jpg",NewImg);

