import math       #to round up can number
def no_of_can(h, w, cov):
    area = h*w
    can = str(math.ceil(area / cov))  #round_up of can calculation.
    
    print("No of cans to cover paint:" + can)

no_of_can(h=100, w=6, cov=20)