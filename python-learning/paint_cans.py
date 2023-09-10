def no_of_can(h, w, cov):
    area = h*w
    can = str(area / cov)
    
    print("No of cans :" + can)

no_of_can(h=100, w=6, cov=20)