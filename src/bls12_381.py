from default import (
    fm,
    hfm,
    co,
    G1,
    G2,
    Z1,
    Z2,
)
from utils import (
    cmp_add,
    cmp_sub,
    cmp_mul,
    cmp_div,
)

# Elliptic Curve(BLS12-381)
# y^2 = x^3 + 4
# or
# Y^2 * Z = X^3 + 4Z^3

# Elliptic curve doubling
# using affine coordinates
# affine coordinates is slower than projective coordinates
def double_p(pt: list[int, int]) -> list[int, int]:
    x, y = pt
    m = 3 * x**2 / (2 * y)
    new_x = m**2 - 2 * x
    new_y = -m * new_x + m * x - y
    return [new_x, new_y]


# double in projective coordinates
# P = [X : Y : Z]
# 2P = [new_X : new_Y : new_Z]
def double(point: list[int, int, int]) -> list[int, int, int]:
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
def add(point1: list[int, int, int], point2: list[int, int, int]) -> list[int, int, int]:
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
def multiply(point: list[int, int, int], scalar: int) -> list[int, int, int]:
    if scalar == 0:
        # Z1
        return [1, 1, 0]
    elif scalar == 1:
        return point
    elif not scalar % 2:
        return multiply(double(point), scalar // 2)
    elif scalar < 0:
        return add(multiply(double(point), int(scalar % co // 2)), point)
    else:
        return add(multiply(double(point), int(scalar // 2)), point)

    
# Field Element
def FE(point_element: int) -> int:
    return point_element % fm


# nomalizer
# projective coordinates -> affine coordinates
# [X : Y : Z] -> [x, y]
def normalize(point: list[int, int, int]) -> list[int, int, int]:
    X, Y, Z = point
    return [FE(X * pow(Z, -1, fm)), FE(Y * pow(Z, -1, fm))]


# check point exists on curve
def on_curve(point: list) -> bool:
    # affine coordinate
    if len(point) == 2:
        x, y = point
        return FE(y**2) == FE(x**3 + 4)
    # projective coordinate
    else:
        X, Y, Z = point
        return FE(Y**2 * Z) == FE(X**3 + 4 * Z**3)

    
# [X : Y : Z] ==> [X : -Y : Z]
def negative(point: list[int, int, int]) -> list[int, int, int]:
    X, Y, Z = point
    return [X, -Y, Z]


#######################################
# 二次拡大体では複素数平面と同様に演算を定義する
#######################################

# double for Quadratic extension field
def double_G2(point: list[int, int, int]) -> list[int, int, int]:
    x = point[0]
    y = point[1]
    z = point[2]
    W = cmp_mul(cmp_mul(3, x), x)
    S = cmp_mul(y, z)
    B = cmp_mul(cmp_mul(x, y), S)
    H = cmp_sub(cmp_mul(W, W), cmp_mul(8, B))
    new_X = cmp_mul(cmp_mul(2, H), S)
    new_Y = cmp_sub(cmp_mul(W, cmp_sub(cmp_mul(4, B), H)),
                    cmp_mul(cmp_mul(cmp_mul(cmp_mul(8, y), y), S), S))
    new_Z = cmp_mul(cmp_mul(8, cmp_mul(S, S)), S)
    return [new_X, new_Y, new_Z]


def add_G2(point1: list[list[int, int], list[int, int], list[int, int]],
           point2: list[list[int, int], list[int, int], list[int, int]]) -> list[list[int, int], list[int, int], list[int, int]]:
    if point1[2] == 0 or point2[2] == 0:
        if point2[2] == 0:
            return point1
        else:
            return point2
    
    X_1, Y_1, Z_1 = point1[0], point1[1], point1[2]
    X_2, Y_2, Z_2 = point2[0], point2[1], point2[2]
    U1 = cmp_mul(Y_2, Z_1)
    U2 = cmp_mul(Y_1, Z_2)
    V1 = cmp_mul(X_2, Z_1)
    V2 = cmp_mul(X_1, Z_2)
    
    if V1 == V2 and U1 == U2:
        return double_G2(point1)
    elif V1 == V2:
        return [[1, 0], [1, 0], [0, 0]]
    U = cmp_sub(U1, U2)
    V = cmp_sub(V1, V2)

    V_squared = cmp_mul(V, V)
    V_squared_times_V2 = cmp_mul(V_squared, V2)
    V_cubed = cmp_mul(V, V_squared)
    W = cmp_mul(Z_1, Z_2)
    A = cmp_sub(cmp_sub(cmp_mul(cmp_mul(U, U), W), V_cubed), cmp_mul(2, V_squared_times_V2))
    
    new_X = cmp_mul(V, A)
    new_Y = cmp_sub(cmp_mul(U, cmp_sub(V_squared_times_V2, A)), cmp_mul(V_cubed, U2))
    new_Z = cmp_mul(V_cubed, W)
    return [new_X, new_Y, new_Z]


def multiply_G2(point: list[list[int, int], list[int, int], list[int, int]],
                scalar: int) -> list[list[int, int], list[int, int], list[int, int]]:
    if scalar == 0:
        # Z2
        return [[1, 0], [1, 0], [0, 0]]
    elif scalar == 1:
        return point
    elif not scalar % 2:
        return multiply_G2(double_G2(point), scalar // 2)
    else:
        return add_G2(multiply_G2(double_G2(point), int(scalar // 2)), point)


#######################################
# pairing on Elliptic curve
#######################################

def pairing():
    return 0
