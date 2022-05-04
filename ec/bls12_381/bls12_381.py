import sympy
from default import (
    fm,
    hfm,
    co,
    G1,
    G2,
    Z1,
    Z2,
)

# Elliptic Curve(BLS12-381)
# y^2 = x^3 + 4
# or
# Y^2

# Elliptic curve doubling
# using affine coordinates
# affine coordinates is slower than projective coordinates
def double_p(pt):
    x, y = pt
    m = 3 * x**2 / (2 * y)
    new_x = m**2 - 2 * x
    new_y = -m * new_x + m * x - y
    return (new_x, new_y)

# double in projective coordinates
# P = [X : Y : Z]
# 2P = [new_X : new_Y : new_Z]
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
# P = [X1 : Y1 : Z1]
# Q = [X2 : Y2 : Z2]
# R = P + Q = [new_X : new_Y : new_Z]
def add(point1, point2) -> int:
    if point1[2] == 0 or point2[2] == 0:
        return point1 if point2[2] == 0 else point2
    X_1, Y_1, Z_1 = point1
    X_2, Y_2, Z_2 = point2
    U1 = Y_2 * Z_1
    U2 = Y_1 * Z_2
    V1 = X_2 * Z_1
    V2 = X_1 * Z_2
    if V1 == V2 and U1 == U2:
        return double(point1)
    elif V1 == V2:
        return [1, 1, 0]
    U = U1 - U2
    V = V1 - V2
    V_squared = V * V
    V_squared_times_V2 = V_squared * V2
    V_cubed = V * V_squared
    W = Z_1 * Z_2
    A = U * U * W - V_cubed - 2 * V_squared_times_V2
    new_X = FE(V * A)
    new_Y = FE(U * (V_squared_times_V2 - A) - V_cubed * U2)
    new_Z = FE(V_cubed * W)
    return [new_X, new_Y, new_Z]

# multiply in projective coordinates
def multiply(point: list, scalar: int) -> list:
    if scalar == 0:
        return [1, 1, 0]
    elif scalar == 1:
        return point
    elif not scalar % 2:
        return multiply(double(point), scalar // 2)
    else:
        return add(multiply(double(point), int(scalar // 2)), point)

# Field Element
def FE(point_element: int) -> int:
    return point_element % fm

# nomalizer
# projective coordinates -> affine coordinates
# [X : Y : Z] -> [x, y]
def normalize(point: list) -> list:
    X, Y, Z = point
    return [FE(X * sympy.mod_inverse(Z, fm)), FE(Y * sympy.mod_inverse(Z, fm))]

# check point exists on curve
def on_curve(point: list) -> bool:
    # affine coordinate
    if (len(point) == 2):
        x, y = point
        return FE(y**2) == FE(x**3 + 4)
    # projective coordinate
    else:
        X, Y, Z = point
        return FE(Y**2 * Z) == FE(X**3 + 4 * Z**3)

def negative(point: list):
    X, Y, Z = point
    return [X, -Y, Z]
