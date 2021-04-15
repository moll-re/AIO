
def clean_axis(x,y):
    """x is the time the point in y was taken"""
    try:
        xn = range(x[0], x[-1]+1)
        yn = []
        count = 0
        for x_i in xn:
            if x_i in x:
                yn.append(y[count])
                count += 1
            else:
                yn.append(0)
        xn = [i - int(x[0]) for i in xn]
    except:
        xn = []
        yn = []
    return xn, yn