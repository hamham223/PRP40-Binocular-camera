from PIL import Image
from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import axes3d
import Homography, Sfm, sift, Camera

K=array([[1.48328735e+03,0.00000000e+00,7.34012939e+02],
[0.00000000e+00,1.48171814e+03,8.59885951e+02],
[0.00000000e+00,0.00000000e+00,1.00000000e+00]]);

print('Step1...',end=' ');
Img1=array(Image.open('../ActiveTest/Left3.jpg'));
sift.ProcessImage('../ActiveTest/Left3.jpg','../ActiveTest/Left3.sift');
L1,D1=sift.ReadFeaturesFromFile('../ActiveTest/Left3.sift');

Img2=array(Image.open('../ActiveTest/Right3.jpg'));
sift.ProcessImage('../ActiveTest/Right3.jpg','../ActiveTest/Right3.sift');
L2,D2=sift.ReadFeaturesFromFile('../ActiveTest/Right3.sift');

print('Finished!');
print('Step2...',end=' ');
Matches=sift.MatchTwoSided(D1,D2);

figure(); gray();
sift.PlotMatches(Img1,Img2,L1,L2,Matches);
show();

Index=Matches.nonzero()[0];
X1=Homography.MakeHomoG(L1[Index,:2].T);
Index2=[int(Matches[i]) for i in Index];
X2=Homography.MakeHomoG(L2[Index2,:2].T);

X1Normal=dot(inv(K),X1);
X2Normal=dot(inv(K),X2);
'''
print('Finished!');
print('Step3...',end=' ');
Model=Sfm.RansacModel();
print(X1Normal.shape);
print(X2Normal.shape);
E,inliers=Sfm.FFromRansac(X1Normal,X2Normal,Model);

print('Finished!');
print('Step4...',end=' ');
P1=array([[1,0,0,0],[0,1,0,0],[0,0,1,0]]);
P2=Sfm.ComputePFromEssential(E);
'''

R=array([[ 0.99763786 , 0.00326705 , 0.06861506],
		[-0.00318983, 0.99999415, -0.00123497],
		[-0.06861869, 0.00101318,  0.99764245]]);
T=array([[ 0.16780832],[-0.01496177],[-0.03598987]]);
RT1=array([[ 0.99763786 , 0.00326705 , 0.06861506,0.16780832 ],
		[-0.00318983,  0.99999415, -0.00123497,-0.01496177],
		[-0.06861869 , 0.00101318,  0.99764245,-0.03598987]]);
RT2=array([[ 0.99763786 , 0.00326705 , 0.06861506,0.16780832 ],
		[-0.00318983,  0.99999415, -0.00123497,-0.01496177],
		[-0.06861869 , 0.00101318,  0.99764245,-0.03598987]]);
Cam1K=array([[1.48328735e+03,0.00000000e+00,7.34012939e+02],
			[0.00000000e+00,1.48171814e+03,8.59885951e+02],
			[0.00000000e+00,0.00000000e+00,1.00000000e+00]]);
Cam2K=array([[1.49549402e+03,0.00000000e+00,7.23153505e+02],
			[0.00000000e+00,1.50254272e+03,8.58920262e+02],
			[0.00000000e+00,0.00000000e+00,1.00000000e+00]]);
P1=dot(Cam1K,RT1);
P2=dot(Cam2K,RT2);
print(P1);
print(P2);
'''
Pos=0; MaxRes=0;
for i in range(4):
    X=Sfm.Triangulate(X1Normal[:,inliers],X2Normal[:,inliers],P1,P2[i]);
    D1=dot(P1,X)[2];
    D2=dot(P2[i],X)[2];
    if sum(D1>0)+sum(D2>0)>MaxRes:
        MaxRes=sum(D1>0)+sum(D2>0);
        Pos=i;
        InFront=(D1>0)&(D2>0);

X=Sfm.Triangulate(X1Normal[:,inliers],X2Normal[:,inliers],P1,P2[Pos]);
X=X[:,InFront];
'''
X=Sfm.Triangulate(X1Normal,X2Normal,P1,P2);

print('Finished!');
print('Step5...',end=' ');
fig=figure();
ax=fig.gca(projection='3d');
ax.plot(-X[0],X[1],X[2],'k.');

Cam1=Camera.Camera(P1);
#Cam2=Camera.Camera(P2[Pos]);
Cam2=Camera.Camera(P2);
X1Points=Cam1.Project(X);
X2Points=Cam2.Project(X);

X1PNormal=dot(K,X1Points);
X2PNormal=dot(K,X2Points);

figure(); imshow(Img1); gray();
plot(X1PNormal[0],X1PNormal[1],'o');
plot(X1[0],X1[1],'r.');
axis('off');

figure(); imshow(Img2); gray();
plot(X2PNormal[0],X2PNormal[1],'o');
plot(X2[0],X2[1],'r.');
axis('off');

show();

print('Finished!');
print('Completed!');