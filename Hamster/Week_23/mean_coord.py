def near(x0,y0,x1,y1):
    #return False
    x0=int(x0);y0=int(y0);x1=int(x1);y1=int(y1)
    dis=abs(x0-x1)+abs(y0-y1)
    _threshold=110
    if abs(x0-x1)>80: return False
    if abs(y0-y1)>80: return False
    return (dis<=_threshold)

def get_coord(goodMatchePoints,k1,k2):
    Left=[];Right=[]
    for i in goodMatchePoints:
        left_id=i.queryIdx
        right_id=i.trainIdx
        xl=int(k1[left_id].pt[0])
        yl=int(k1[left_id].pt[1])
        xr=int(k2[right_id].pt[0])
        yr=int(k2[right_id].pt[1])
        boo=0
        for j in range(len(Left)):
            for k in range(len(Left[j])):
                if near(xl,yl,Left[j][k][0],Left[j][k][1]):
                    Left[j].append([xl,yl]);Right[j].append([xr,yr]);boo=1;break
            if (boo==1) : break
        #for j in Left:
        #    for k in j:
        #        if near(xl,yl,k[0],k[1]): 
        #            j.append([xl,yl]);boo=1;break
        #    if (boo==1) : break
        if (boo==0):
            Left.append([[xl,yl]])
            Right.append([[xr,yr]])
        boo=0
        #for j in Right:
        #    for k in j:
        #        if near(xr,yr,k[0],k[1]): 
        #            j.append([xr,yr]);boo=1;break
        #    if (boo==1) : break
        #if (boo==0):
        #    Right.append([[xr,yr]])
    print(len(Left),len(Right))
    return [Left,Right]

