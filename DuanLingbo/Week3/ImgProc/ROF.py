'''Rudin-Osher-Fatemi(ROF) 去噪模型'''
from numpy import *

def denoise(Img,UInit,Tolerance=0.1,Step=0.125,TVWeight=100):
    m,n=Img.shape;
    U,Px,Py,Error=UInit,Img,Img,1;
    while (Error>Tolerance):
        UOld=U;
        GradUx=roll(U,-1,axis=1)-U;
        GradUy=roll(U,-1,axis=0)-U;

        PxNew=Px+(Step/TVWeight)*GradUx;
        PyNew=Py+(Step/TVWeight)*GradUy;
        NormNew=maximum(1,sqrt(PxNew**2+PyNew**2));

        Px,Py=PxNew/NormNew,PyNew/NormNew;
        RxPx,RyPy=roll(Px,1,axis=1),roll(Py,1,axis=0);

        DivP=(Px-RxPx)+(Py-RyPy);
        U=Img+TVWeight*DivP;

        Error=linalg.norm(U-UOld)/sqrt(n*m);

    return U,Img-U;
