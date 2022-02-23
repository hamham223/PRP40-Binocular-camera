from PIL import Image
from numpy import *
from pylab import *
import os

def ProcessImage(ImgName,ResultName,Params="--edge-thresh 10 --peak-thresh 5"):
    if ImgName[-3:]!='pgm':
        Img=Image.open(ImgName).convert('L');
        ImgName=ImgName[:-3]+'pgm';
        Img.save(ImgName);
    cmmd=str("sift "+ImgName+" --output="+ResultName+" "+Params);
    os.system(cmmd);
    print("Processed",ImgName,"To",ResultName);

def ReadFeaturesFromFile(FileName):
    f=loadtxt(FileName);
    return f[:,:4],f[:,4:];

def WriteFeaturesToFile(FileName,Locs,Desc):
    savetxt(FileName,hstack((Locs,Desc)));

def PlotFeatures(Img,Locs,Circle=False):
    def DrawCircle(c,r):
        t=arange(0,1.01,0.01)*2*pi;
        x=r*cos(t)+c[0];
        y=r*sin(t)+c[1];
        plot(x,y,'b',linewidth=2);
    
    imshow(Img);
    if Circle:
        for p in Locs:
            DrawCircle(p[:2],p[2]);
    else:
        plot(Locs[:,0],locs[:,1],'ob');
    axis('off');

def Match(Desc1,Desc2):
    Desc1=array([d/linalg.norm(d) for d in Desc1]);
    Desc2=array([d/linalg.norm(d) for d in Desc2]);

    DistRatio=0.6;
    DescSize=Desc1.shape;

    MatchScores=zeros((DescSize[0],1),'int');
    Desc2T=Desc2.T;
    for i in range(DescSize[0]):
        DotProds=0.9999*dot(Desc1[i,:],Desc2T);
        Index=argsort(arccos(DotProds));
        
        if arccos(DotProds)[Index[0]]<DistRatio*arccos(DotProds)[Index[1]]:
            MatchScores[i]=int(Index[0]);

    return MatchScores;

def MatchTwoSided(Desc1,Desc2):
    Matches12=Match(Desc1,Desc2);
    Matches21=Match(Desc2,Desc1);

    Index12=Matches12.nonzero()[0];

    for i in Index12:
        if Matches21[int(Matches12[i])]!=i:
            Matches12[i]=0;

    return Matches12;

def AppendImages(Img1,Img2):
    Rows1=Img1.shape[0];
    Rows2=Img2.shape[0];

    if Rows1<Rows2:
        Img1=concatenate((Img1,zeros((Rows2-Rows1,Img1.shape[1]))),axis=0);
    elif Rows1>Rows2:
        Img2=concatenate((Img2,zeros((Rows1-Rows2,Img2.shape[1]))),axis=0);

    return concatenate((Img1,Img2),axis=1);

def PlotMatches(Img1,Img2,Locs1,Locs2,MatchScores,ShowBelow=True):
    Img3=AppendImages(Img1,Img2);
    if ShowBelow:
        Img3=vstack((Img3,Img3));

    imshow(Img3);

    cols1=Img1.shape[1];
    for i,m in enumerate(MatchScores):
        if m[0]>0:
            plot([Locs1[i][0],Locs2[m[0]][0]+cols1],[Locs1[i][1],Locs2[m[0]][1]],'c');
    axis('off');

