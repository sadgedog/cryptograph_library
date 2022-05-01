import time
import sys
import os
from py_ecc import optimized_bls12_381 as opt
from py_ecc import bls12_381 as b

# y^2 = x^3 + 4 (mod p)
# Y^2 * Z = X^3 + 4Z^3 (mod p)
p = 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787
# hexadecimal p
pp = "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab"

# base point
G1 = [
    3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507,
    1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569,
    1
]

argv = sys.argv

# Elliptic curve doubling
# using affine coordinates
# affine coordinates is slower than projective coordinates
def double_p(pt):
    x, y = pt
    m = 3 * x**2 / (2 * y)
    newx = m**2 - 2 * x
    newy = -m * newx + m * x - y
    return (newx, newy)

# double in projective coordinates
# P = [X : Y : Z]
# 2P = [new_X : new_Y3 : new_Z3]
def double(point):
    X, Y, Z = point
    W = 3 * X ** 2
    S = Y * Z
    B = X * Y * S
    H = W * W - 8 * B
    new_X = FE(2 * H * S)
    new_Y = FE(W * (4 * B - H) - 8 * Y ** 2 * S ** 2)
    new_Z = FE(8 * S ** 3)
    return [new_X, new_Y, new_Z]

# add in projective coordinates
# P = [X : Y : Z]
# Q = [X' : Y' : Z']
# R = P + Q = [new_X : new_Y : new_Z]
def add(point1, point2):
    X1, Y1, Z1 = point1
    X2, Y2, Z2 = point2
    U1 = Y2 * Z1
    U2 = Y1 * Z2
    V1 = X2 * Z1
    V2 = X1 * Z2
    if V1 == V2 and U1 == U2:
        return double(point1)
    elif V1 == V2:
        return [1, 1, 0]
    U = U1 - U2
    V = V1 - V2
    V_squared = V * V
    V_squared_times_V2 = V_squared * V2
    V_cubed = V * V_squared
    W = Z1 * Z2
    A = U * U * W - V_cubed - 2 * V_squared_times_V2
    new_X = FE(V * A)
    new_Y = FE(U * (V_squared_times_V2 - A) - V_cubed * U2)
    new_Z = FE(V_cubed * W)
    return [new_X, new_Y, new_Z]

# multiply in projective coordinates
def multiply(point, scalar):
    if scalar == 0:
        return [1, 1, 0]
    elif scalar == 1:
        return point
    elif not scalar % 2:
        return multiply(double(point), scalar // 2)
    else:
        return add(multiply(double(point), int(scalar // 2)), point)

# Field Element
def FE(point_element):
    return point_element % p


# time counter 
def time_cnt(func, p):
    s = time.perf_counter()
    func(p, p)
    e = time.perf_counter()
    print(e - s)
