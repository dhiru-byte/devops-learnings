import math
def no_of_can(h, w, cov):
    area = h*w
    can = str(math.ceil(area / cov))
    
    print("No of cans :" + can)

no_of_can(h=100, w=6, cov=20)