def ifblack(color):
    total=int(color[0])+int(color[1])+int(color[2])
    _threshold=30
    return (total<_threshold)

def exist_line(img,x1,y1,x2,y2):
    if (x1==x2) & (y1==y2): return False
    cut = 10 #cut into (cut-1) pieces
    delta_x=int((x2-x1)/cut)
    delta_y=int((y2-y1)/cut)
    count=0
    for i in range(1,cut):
        x=x1+delta_x*i;y=y1+delta_y*i
        if (ifblack(img[y][x])):count+=1
    return (count<3)
