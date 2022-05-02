# test calc for bls12-381 elliptic curve
import secrets
import random
from py_ecc import optimized_bls12_381 as opt
from bls12_381 import (
    add,
    double,
    multiply,
    normalize,
)
from default import (
    fm,
    hfm,
    co,
    G1,
    G2,
    Z1,
    Z2,
)
from lagrange import (
    generate_share,
    elliptic_lagrange,
    elliptic_lagrange_coef,
)

# reference
def double_ref(point):
    return opt.double(point)

def add_ref(point1, point2):
    return opt.add(point1, point2)

def multiply_ref(point, scalar):
    return opt.multiply(point, scalar)

def check(expected, mode, i1, i2, i3, i4, i5, i6, s):
    if (mode == "double"):
        r = double([i1, i2, i3])
        if (r == list(expected)):
            print(expected, "\n=>", r)
            print("OK\n")
        else:
            print("expected", expected, "\nbut got", r)
    if (mode == "add"):
        r = add([i1, i2, i3], [i4, i5, i6])
        if (r == list(expected)):
            print(expected, "\n=>", r)
            print("OK\n")
        else:
            print("expected", expected, "\nbut got", r)
    if (mode == "multiply"):
        r = multiply([i1, i2, i3], s)
        if (r == list(expected)):
            print(expected, "\n=>", r)
            print("OK\n")
        else:
            print("expected", expected, "\nbut got", r)

def rnd_scalar():
    return secrets.randbelow(co)

# check calc result using py_ecc optimized bls12-381 library
def main():
    # calculate tests
    cnt = 0
    while(cnt < 10):
        cnt += 1
        s = rnd_scalar()
        check(double_ref(opt.G1), "double", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
        check(add_ref(opt.G1, opt.G1), "add", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
        check(multiply_ref(opt.G1, s), "multiply", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
        
    #############################################################################
    # 一般的なラグランジュ補間では, xy平面上のn次関数f(x)をf(x)上のn-1点から復元する.
    # n次関数f(x)を(x, f(x)*G1)と定義することで, 楕円曲線上でラグランジュ補間を行える.
    #############################################################################
    # 楕円曲線上のラグランジュ補間のテスト
    # 補間する楕円曲線上の点をs11とし, 閾値k = 8とする.
    # elliptic lagrange test
    # (scalar, elliptic point)
    cnt = 0
    while (cnt < 10):
        cnt += 1
        n = 10
        k = 8
        # share
        share, pcoef = generate_share(rnd_scalar(), n, k)
        # want to interpolate s11
        s11 = [1, multiply(G1, share[0])]
        
        s12 = [2, multiply(G1, share[1])]
        s13 = [3, multiply(G1, share[2])]
        s14 = [4, multiply(G1, share[3])]
        s15 = [5, multiply(G1, share[4])]
        s16 = [6, multiply(G1, share[5])]
        s17 = [7, multiply(G1, share[6])]
        s18 = [8, multiply(G1, share[7])]
        s19 = [9, multiply(G1, share[8])]
        s110 = [10, multiply(G1, share[9])]

        # k = 8
        ls = [s13, s12, s110, s14, s19, s17, s18, s15]
        # interpolate f(x = 1)
        RS = elliptic_lagrange(1, ls, "Z1")
        print(normalize(RS))
        print(normalize(s11[1]))

        if(normalize(RS) == normalize(s11[1])):
            print("OK")

    
main()
