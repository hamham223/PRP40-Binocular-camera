from PIL import Image
from numpy import *
from pylab import *

def Normalize(Points):
    '''在齐次坐标意义下，对点集进行归一化，使最后一行为1'''
    for Row in Points:
        Row/=Points[-1]+1e-9;
    return Points;

def MakeHomoG(Points):
    '''将点集(dim*n)转换为齐次坐标表示'''
    return vstack((Points,ones((1,Points.shape[1]))));

def HFromPoints(fp,tp):
    '''使用线性DLT方法，计算单应性矩阵H，使fp映射到tp。点自动进行归一化'''
    if fp.shape!=tp.shape:
       raise RuntimeError('Number Of Points Do Not Match!');

    M=mean(fp[:2],axis=1);
    Maxstd=max(std(fp[:2],axis=1))+1e-9;
    C1=diag([1/Maxstd,1/Maxstd,1]);
    C1[0][2]=-M[0]/Maxstd;
    C1[1][2]=-M[1]/Maxstd;
    fp=dot(C1,fp);

    M=mean(tp[:2],axis=1);
    Maxstd=max(std(tp[:2],axis=1))+1e-9;
    C2=diag([1/Maxstd,1/Maxstd,1]);
    C2[0][2]=-M[0]/Maxstd;
    C2[1][2]=-M[1]/Maxstd;
    tp=dot(C2,tp);

    NumCorrespondences=fp.shape[1];
    A=zeros((2*NumCorrespondences,9));
    for i in range(NumCorrespondences):
        A[2*i]=[-fp[0][i],-fp[1][i],-1,0,0,0,tp[0][i]*fp[0][i],tp[0][i]*fp[1][i],tp[0][i]];
        A[2*i+1]=[0,0,0,-fp[0][i],-fp[1][i],-1,tp[1][i]*fp[0][i],tp[1][i]*fp[1][i],tp[1][i]];

    U,S,V=linalg.svd(A);
    H=V[8].reshape((3,3));

    H=dot(linalg.inv(C2),dot(H,C1));

    return H/H[2,2];

def HaffineFromPoints(fp,tp):
    '''计算H，仿射变换，使得tp是fp进过仿射变换H得到的'''
    if fp.shape!=tp.shape:
       raise RuntimeError('Number of Points do NOT Match!');

    M=mean(fp[:2],axis=1);
    Maxstd=max(std(fp[:2],axis=1))+1e-9;
    C1=diag([1/Maxstd,1/Maxstd,1]);
    C1[0][2]=-M[0]/Maxstd;
    C1[1][2]=-M[1]/Maxstd;
    fp_cond=dot(C1,fp);

    M=mean(tp[:2],axis=1);
    C2=C1.copy();
    C2[0][2]=-M[0]/Maxstd;
    C2[1][2]=-M[1]/Maxstd;
    tp_cond=dot(C2,tp);

    A=concatenate((fp_cond[:2],tp_cond[:2]),axis=0);
    U,S,V=linalg.svd(A.T);

    tmp=V[:2].T;
    B=tmp[:2];
    C=tmp[2:4];

    tmp2=concatenate((dot(C,linalg.pinv(B)),zeros((2,1))),axis=1);
    H=vstack((tmp2,[0,0,1]));

    H=dot(linalg.inv(C2),dot(H,C1));

    return H/H[2,2];

def HFromRansac(fp,tp,Model,MaxIter=1000,MatchTheshold=10):
    '''使用RANSAC稳健性估计点对应间的但对应性矩阵H'''
    import ransac

    Data=vstack((fp,tp));
    
    H,RansacData=ransac.ransac(Data.T,Model,4,MaxIter,MatchTheshold,10,return_all=True);
    return H,RansacData['inliers'];

class RansacModel(object):
    '''用于测试单应性矩阵的类，其中单应性矩阵由ransac.py计算'''

    def __init__(self,debug=False):
        self.debug=debug;

    def fit(self,Data):
        Data=Data.T;

        fp=Data[:3,:4];
        tp=Data[3:,:4];

        return HFromPoints(fp,tp);

    def get_error(self,Data,H):
        Data=Data.T;

        fp=Data[:3];
        tp=Data[3:];

        fpTrans=dot(H,fp);

        for i in range(3):
            fpTrans[i]/=fpTrans[2]+1e-9;
            
        return sqrt(sum((tp-fpTrans)**2,axis=0));






