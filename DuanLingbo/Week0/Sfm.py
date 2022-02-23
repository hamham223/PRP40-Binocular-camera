from PIL import Image
from numpy import *
from pylab import *

def ComputeFundamental(X1,X2):
    '''使用归一化的八点算法，从对应点（X1,X2）中计算基础矩阵，每行有如下构成[X'*X,X'*Y'X',Y'*X,Y'*Y,X,Y,1]'''
    N=X1.shape[1];
    if X2.shape[1]!=N:
        raise ValueError("Number of Points DON'T Match!");

    A=zeros((N,9));
    for i in range(N):
        A[i]=[X1[0,i]*X2[0,i],X1[0,i]*X2[1,i],X1[0,i]*X2[2,i],
            X1[1,i]*X2[0,i],X1[1,i]*X2[1,i],X1[1,i]*X2[2,i],
            X1[2,i]*X2[0,i],X1[2,i]*X2[1,i],X1[2,i]*X2[2,i]];

    U,S,V=linalg.svd(A);
    F=V[-1].reshape(3,3);
    
    U,S,V=linalg.svd(F);
    S[2]=0;
    F=dot(U,dot(diag(S),V));

    return F/F[2,2];

def ComputeFundamentalNormalized(X1,X2):
    '''使用归一化的八点算法，用对应点计算基础矩阵'''
    N=X1.shape[1];
    if X2.shape[1]!=N:
        raise ValueError("Number of Points DON'T Match!");

    X1=X1/X1[2];
    Mean1=mean(X1[:2],axis=1);
    S1=sqrt(2)/std(X1[:2]);
    T1=array([[S1,0,-S1*Mean1[0]],[0,S1,-S1*Mean1[1]],[0,0,1]]);
    X1=dot(T1,X1);

    X2=X2/X2[2];
    Mean2=mean(X2[:2],axis=1);
    S2=sqrt(2)/std(X2[:2]);
    T2=array([[S2,0,-S2*Mean2[0]],[0,S2,-S2*Mean2[1]],[0,0,1]]);
    X2=dot(T2,X2);

    F=ComputeFundamental(X1,X2);
    F=dot(T1.T,dot(F,T2));

    return F/F[2,2];

def ComputeEpipole(F):
    '''从基础矩阵F中计算右极点（可以使用F.T获得左极点）'''
    U,S,V=linalg.svd(F);
    e=V[-1];
    return e/e[2];

def PlotEpipolarLine(Img,F,X,Epipole=None,ShowEpipole=True):
    '''在图像中，绘制外极点和外极线Fx=0。F为基础矩阵，x为另一幅图像中的点'''
    m,n=Img.shape[:2];
    Line=dot(F,X);

    T=linspace(0,n,100);
    LineT=array([(Line[2]+Line[0]*Tt)/(-Line[1]) for Tt in T]);

    Index=(LineT>=0)&(LineT<m);
    plot(T[Index],LineT[Index],linewidth=2);

    if ShowEpipole:
        if Epipole is None:
            Epipole=ComputeEpipole(F);
        plot(Epipole[0]/Epipole[2],Epipole[1]/Epipole[2],'r*');

def TriangulatePoint(X1,X2,P1,P2):
    '''使用最小二乘解，绘制点对的三角剖分'''
    M=zeros((6,6));
    M[:3,:4]=P1; M[3:,:4]=P2;
    M[:3,4]=-X1; M[3:,5]=-X2;

    U,S,V=linalg.svd(M);
    X=V[-1,:4];
    return X/X[3];

def Triangulate(X1,X2,P1,P2):
    '''X1和X2中点的二视图三角剖分'''
    N=X1.shape[1];
    if X2.shape[1]!=N:
        raise ValueError("Number of Points DON'T Match!");

    X=[TriangulatePoint(X1[:,i],X2[:,i],P1,P2) for i in range(N)];
    return array(X).T;

def ComputeP(x,X):
    '''由二维-三维对应对计算照相机矩阵'''
    n=x.shape[1];
    if X.shape[1]!=n:
        raise ValueError("Number of Points DON'T Match!");

    M=zeros((3*n,12+n));
    for i in range(n):
        M[3*i,0:4]=X[:,i];
        M[3*i+1,4:8]=X[:,i];
        M[3*i+2,8:12]=X[:,i];
        M[3*i:3*i+3,i+12]=-x[:,i];

    U,S,V=linalg.svd(M);
    return V[-1,:12].reshape((3,4));

def ComputePFromFundamental(F):
    '''从基础矩阵中计算第二个照相机矩阵'''
    E=ComputeEpipole(F.T);
    TE=Skew(E);
    return vstack((dot(TE,F.T).T,E)).T;

def Skew(A):
    '''反对称矩阵B，使得对于每个v有A*v=Bv'''
    return array([[0,-A[2],A[1]],[A[2],0,-A[0]],[-A[1],A[0],0]]);

def ComputePFromEssential(E):
    '''从本质矩阵中计算第二个照相机矩阵（假设P1=[I 0]）
       输出为4个可能的照相机矩阵列表'''
    U,S,V=svd(E);
    if det(dot(U,V))<0:
        V=-V;
    E=dot(U,dot(diag([1,1,0]),V));

    Z=Skew([0,0,-1]);
    W=array([[0,-1,0],[1,0,0],[0,0,1]]);

    P2=[vstack((dot(U,dot(W,V)).T,U[:,2])).T,
        vstack((dot(U,dot(W,V)).T,-U[:,2])).T,
        vstack((dot(U,dot(W.T,V)).T,U[:,2])).T,
        vstack((dot(U,dot(W.T,V)).T,-U[:,2])).T];
    return P2;

def FFromRansac(X1,X2,Model,MaxIter=5000,MatchTheshold=1e-6):
    '''使用RANSAC方法从点对应中稳健的估计基础矩阵F
       输入：使用齐次坐标表示的点X1,X2（3*n）'''
    import ransac

    Data=vstack((X1,X2));
    F,RansacData=ransac.ransac(Data.T,Model,8,MaxIter,MatchTheshold,20,return_all=True);
    return F,RansacData['inliers'];

class RansacModel(object):
    '''用于计算基础矩阵的类'''
    def __init__(self,debug=False):
        self.debug=debug;

    def fit(self,Data):
        '''使用选择的8个对应计算基础矩阵'''
        Data=Data.T;
        X1=Data[:3,:8];
        X2=Data[3:,:8];

        F=ComputeFundamentalNormalized(X1,X2);
        return F;

    def get_error(self,Data,F):
        '''计算所有对应的x^T F x，并返回每个变换后点的误差'''
        Data=Data.T;
        X1=Data[:3]; 
        X2=Data[3:];

        Fx1=dot(F,X1);
        Fx2=dot(F,X2);
        denom=Fx1[0]**2+Fx1[1]**2+Fx2[0]**2+Fx2[1]**2;
        Err=(diag(dot(X1.T,dot(F,X2))))**2/denom;

        return Err;




