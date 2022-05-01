# test calc for bls12-381 elliptic curve
import sys
import secrets
from py_ecc import optimized_bls12_381 as opt
import bls12_381 as test

argv = sys.argv
p = 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787
G1 = [
    3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507,
    1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569,
    1
]

# reference
def double_ref(point):
    return opt.double(point)

def add_ref(point1, point2):
    return opt.add(point1, point2)

def multiply_ref(point, scalar):
    return opt.multiply(point, scalar)

def check(expected, mode, i1, i2, i3, i4, i5, i6, s):
    if (mode == "double"):
        r = test.double([i1, i2, i3])
        if (r == list(expected)):
            print(expected, "\n=>", r)
        else:
            print("expected", expected, "\nbut got", r)
    if (mode == "add"):
        r = test.add([i1, i2, i3], [i4, i5, i6])
        if (r == list(expected)):
            print(expected, "\n=>", r)
        else:
            print("expected", expected, "\nbut got", r)
    if (mode == "multiply"):
        r = test.multiply([i1, i2, i3], s)
        if (r == list(expected)):
            print(expected, "\n=>", r)
        else:
            print("expected", expected, "\nbut got", r)

def rnd_scalar():
    return secrets.randbelow(p)

# check calc result using py_ecc optimized bls12-381 library
def main():
    s = rnd_scalar()
    check(double_ref(opt.G1), "double", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
    check(add_ref(opt.G1, opt.G1), "add", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
    check(multiply_ref(opt.G1, s), "multiply", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)

    while (True):
        s = rnd_scalar()
        check(multiply_ref(opt.G1, s), "multiply", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)

main()
