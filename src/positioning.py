import math

L1 = 30 #length of arm 1
L2 = 30 #length of arm 2

def moveTo(x,y,z):
    if( x == 0 ):
        gamma = math.pi/2
        D = y
    else:
        gamma = math.atan(y/x)
        D = x/math.cos(gamma)
    H = math.sqrt(D*D + z*z)
    alpha = math.acos((L2*L2 - L1*L1 - H*H)/(-2*L1*H))
    beta = math.acos((H*H - L2*L2 - L1*L1)/(-2*L1*L2))
    alpha2 = alpha + math.atan(z/H)
    print('alpha2')
    print(deg(alpha2))
    print('beta')
    print(deg(beta))
    print('gamma')
    print(deg(gamma))

def deg(angle):
    return 180*angle/math.pi
