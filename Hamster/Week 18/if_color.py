def ifblue(color):
    expect=[167,93,55];diff=0
    for i in range(3):
        diff+=abs(expect[i]-int(color[i]))
    thershold=110
    return (diff<=thershold)

def ifgreen(color):
    expect=[50,95,59];diff=0
    if color[0]>=100: return False
    for i in range(3):
        diff+=abs(expect[i]-int(color[i]))
    thershold=135
    return (diff<=thershold)