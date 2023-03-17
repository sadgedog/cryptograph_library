# util functions
import time
import secrets
from default import (
    fm,
    co,
    G1,
    G2,
    Z1,
    Z2,
)

# time counter 
def time_cnt(func, p):
    s = time.perf_counter()
    func(p, p)
    e = time.perf_counter()
    print(e - s)

def rnd_scalar():
    return secrets.randbelow(co)
    
# Field Element
def FE(point_element: int) -> int:
    return point_element % fm


def cmp_add(a, b):
    if type(a) == list and type(b) == list:
        return [FE(a[0] + b[0]), FE(a[1] + b[1])]
    elif type(a) == int and type(b) == list:
        return [FE(a + b[0]), FE(b[1])]
    elif type(a) == list and type(b) == int:
        return [FE(b + a[0]), FE(a[1])]
    else:
        exit(1)

        
def cmp_sub(a, b):
    if type(a) == list and type(b) == list:
        return [FE(a[0] - b[0]), FE(a[1] - b[1])]
    elif type(a) == int and type(b) == list:
        return [FE(a - b[0]), FE(b[1])]
    elif type(a) == list and type(b) == int:
        return [FE(b - a[0]), FE(a[1])]
    else:
        exit(1)

        
def cmp_mul(a, b):
    if type(a) == list and type(b) == list:
        return [FE(a[0] * b[0] - a[1] * b[1]), FE(a[0] * b[1] + a[1] * b[0])]
    elif type(a) == int and type(b) == list:
        return [FE(a * b[0]), FE(a * b[1])]
    elif type(a) == list and type(b) == int:
        return [FE(b * a[0]), FE(b * a[1])]
    else:
        exit(1)

        
def cmp_div(a, b):
    if type(a) == list and type(b) == list:
        r = FE(a[0] * b[0] + a[1] * b[1]) * pow(b[0]**2 + b[1]**2, -1, fm)
        c = FE(a[1] * b[0] + a[0] * b[1]) * pow(b[0]**2 + b[1]**2, -1, fm)
        return [FE(r), FE(c)]
    elif type(a) == int and type(b) == list:
        return [b[0] * pow(a, -1, fm), b[1] * pow(a, -1, fm)]
    elif type(a) == list and type(b) == int:
        return [a[0] * pow(b, -1, fm), a[1] * pow(b, -1, fm)]
    else:
        exit(1)


# FQ2では拡大体の要素が取り出せないので、strキャストして無理やり変換しています
def FQ2_to_list(h2):
    a = list(map(str, h2))
    x1, y1 = "", ""
    x2, y2 = "", ""
    x3, y3 = "", ""  
    for i in range(200):
        if a[0][i+1] == ",":
            y1 = a[0][i+3:len(a[0])-1]
            break
        else:
            x1 += a[0][i+1]
    for i in range(200):
        if a[1][i+1] == ",":
            y2 = a[1][i+3:len(a[1])-1]
            break
        else:
            x2 += a[1][i+1]
    for i in range(200):
        if a[2][i+1] == ",":
            y3 = a[2][i+3:len(a[2])-1]
            break
        else:
            x3 += a[2][i+1]
    h2 = [[int(x1), int(y1)], [int(x2), int(y2)],[int(x3), int(y3)]]
    return h2
