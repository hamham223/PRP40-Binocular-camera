
def if_blue(color):
    if (color[0]>=180 )& (color[2]<=30): return True
    orange=[165,60,0]
    diff=abs(int(color[2])-int(orange[2]))*0.1+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.6
    threshold=30
    return (diff<=threshold)

