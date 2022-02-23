from numpy import true_divide
import math

pi=3.14159
def score(a,b):
    a=int(a);b=int(b)
    if 2*a<b: return 1
    if 1.3*a<b: return 0.6
    if a<b: return 0.3
    return 0

def ifblack(color):
    total=int(color[0])+int(color[1])+int(color[2])
    _threshold=50
    return score(total,_threshold)

def ifwhite(color):
    total=255*3-int(color[0])-int(color[1])-int(color[2])
    _threshold=120
    return score(total,_threshold)

def slope(x1,y1,x2,y2):
    s=math.atan2(y2-y1,x2-x1)
    s=abs(s)/pi*180
    if (abs(s-80))<20: return True
    if (abs(s-25))<40: return True
    if (abs(s)<3): return True
    return False
def exist_line(img,x1,y1,x2,y2):
    if (x1==x2) & (y1==y2): return False
    #if not slope(x1,y1,x2,y2): return False
    cut = 60 #cut into (cut-1) pieces
    delta_x=(x2-x1)/cut
    delta_y=(y2-y1)/cut
    count=0
    for i in range(2,cut):
        x=x1+delta_x*i;y=y1+delta_y*i
        x=int(x);y=int(y)
        temp=ifblack(img[y][x])
        #if temp==0: return False
        count=count+temp
    if (count>12):return False
    #count=0
    #for i in range(3,cut-2):
    #    x=x1+delta_x*i;y=y1+delta_y*i+10
    #    temp=ifwhite(img[y][x])
    #    if temp==0: return False
    #    count=count+temp
    #if (count>6):return True
    #count=0
    #for i in range(3,cut-2):
    #    x=x1+delta_x*i+10;y=y1+delta_y*i
    #    temp=ifwhite(img[y][x])
    #    if temp==0: return False
    #    count=count+temp
    #if (count>6):return True
    return True