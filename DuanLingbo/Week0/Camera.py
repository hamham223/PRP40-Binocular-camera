from numpy import *
from pylab import *
from PIL import Image
from scipy import linalg

class Camera(object):
    '''针孔照相机'''

    def __init__(self,P):
        self.P=P;
        self.K=None; self.R=None; self.t=None; self.c=None;

    def Project(self,X):
        '''X的投影点，并进行坐标归一化'''
        x=dot(self.P,X);
        for i in range(3):
            x[i]/=x[2]+1e-9;
        return x;

    def Factor(self):
        '''将照相机矩阵分解为K,R,t,其中R=K[R|t]'''

        K,R=linalg.rq(self.P[:,:3]);

        T=diag(sign(diag(K)));
        if linalg.det(T)<0:
            T[1,1]*=-1;

        self.K=dot(K,T);
        self.R=dot(T,R);
        self.t=dot(linalg.inv(self.K),self.P[:,3]);

        return self.K,self.R,self.t;

    def Center(self):
        '''计算并返回照相机的中心'''
        if self.c is not None:
           return self.c;
        else:
            self.factor();
            self.c=-dot(self.R.T,self.t);
            return self.c;

def RotationMatrix(A):
    '''创建一个用于围绕向量A轴旋转的三维旋转矩阵'''
    R=eye(4);
    R[:3,:3]=linalg.expm([[0,-A[2],A[1]],[A[2],0,-A[0]],[-A[1],A[0],0]]);
    return R;

def rq(A):
    from scipy.linalg import qr
    
    Q,R = qr(flipud(A).T)
    R = flipud(R.T)
    Q = Q.T
    
    return R[:,::-1],Q[::-1,:]

    

