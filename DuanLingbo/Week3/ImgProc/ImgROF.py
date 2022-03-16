from PIL import Image
from pylab import *
import ROF
from numpy import *
from numpy import random

Img=array(Image.open("../Photo/ImgGausFilter_1.jpg"));
U=T=zeros(Img.shape);
for i in range(3):
    U[:,:,i],T[:,:,i]=ROF.denoise(Img[:,:,i],Img[:,:,i]);
    #U[:,:,i]=U[:,:,i]*(U[:,:,i]>=5); 
    #U[:,:,i]=U[:,:,i]*(U[:,:,i]<=240);

figure(); 
subplot(2,4,1); imshow(Img); title("Img");
subplot(2,4,3); imshow(U.astype(uint8)); title("ROF");
show();

imsave('../Photo/ImgROF_1.jpg',U.astype(uint8));
