
def if_orange(color):
    orange=[3,140,248]
    diff=abs(int(color[2])-int(orange[2]))*0.6+abs(int(color[1])-int(orange[1]))*0.3+abs(int(color[0])-int(orange[0]))*0.1
    threshold=50
    return (diff<=threshold)

