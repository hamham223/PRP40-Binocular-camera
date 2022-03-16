import os
from PIL import Image
from pylab import *
from numpy import *

def GetImgList(Path):
    return [os.path.join(Path,f) for f in os.listdir(Path) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.ppm')];

def HistEq(Img,Nbr_Bins=256):
    ''' Cumulative Distribution Function '''
    ImgHist,Bins=histogram(Img.flatten(),Nbr_Bins,normed=True);
    cdf=ImgHist.cumsum();
    cdf=255*cdf/cdf[-1];
    NewImg=interp(Img.flatten(),Bins[:-1],cdf);
    return NewImg.reshape(Img.shape),cdf;

def ComputeAvgImg(ImgList):
    AvgImg=array(Image.open(ImgList[0]),'f');
    for ImgName in ImgList[1:]:
        try:
            AvgImg+=array(Image.open(ImgName));
        except:
            print(ImgName+"...Skipped");
    AvgImg/=len(ImgList);
    return array(AvgImg,'uint8');

def Plot2DBoundary(PlotRange,Points,DecisionFcn,Labels,Values=[0]):
    '''PlotRange为画图范围，Points为类数据点列表,DecisionFcn是评估函数,Labels是函数DecisionFcn关于每个类返回的标记列表'''

    ColList=['b','r','g','k','m','y'];
    X=arange(PlotRange[0],PlotRange[1],.1);
    Y=arange(PlotRange[2],PlotRange[3],.1);
    x,y=meshgrid(X,Y);
    xList,yList=x.flatten(),y.flatten();
    z=array(DecisionFcn(xList,yList));
    z=z.reshape(x.shape);
    contour(x,y,z,Values);

    for i in range(len(Points)):
        D=DecisionFcn(Points[i][:,0],Points[i][:,1]);
        CorrectIndex=Labels[i]==D;
        InCorrectIndex=Labels[i]!=D;
        plot(Points[i][CorrectIndex,0],Points[i][CorrectIndex,1],'*',color=ColList[i]);
        plot(Points[i][InCorrectIndex,0],Points[i][InCorrectIndex,1],'o',color=ColList[i]);

    axis('equal');

def ImgResize(Img,Size):
    '''图像尺寸调整'''
    PILImg=Image.fromarray(uint8(Img));
    return array(PILImg.resize(Size));

if __name__=='__main__':
    print(GetImgList('../Collect'));


