# test calc for bls12-381 elliptic curve
import random
import string
import secrets
import sympy
from py_ecc import optimized_bls12_381 as opt
from bls12_381 import (
    add,
    double,
    multiply,
    normalize,
    on_curve,
    double_G2,
    add_G2,
    multiply_G2,
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
from elgamal import (
    key_generator,
    encrypt,
    decrypt,
)
from utils import (
    FQ2_to_list,
)

import rsa
import he

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


def rnd_str(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)


def calc_test():
    # calculate tests
    cnt = 0
    while cnt < 10:
        cnt += 1
        s = rnd_scalar()
        check(double_ref(opt.G1), "double", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
        check(add_ref(opt.G1, opt.G1), "add", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
        check(multiply_ref(opt.G1, s), "multiply", G1[0], G1[1], G1[2], G1[0], G1[1], G1[2], s)
    print("elliptic calc: OK")

    
def elliptic_lagrange_test():
    #############################################################################
    # 一般的なラグランジュ補間では, xy平面上のn次関数f(x)をf(x)上のn-1点から復元する.
    # n次関数f(x)を(x, f(x)*G1)と定義することで, 楕円曲線上でラグランジュ補間を行える.
    #############################################################################
    # 楕円曲線上のラグランジュ補間のテスト
    # 簡単のため, 補間する楕円曲線上の点をs11とし, 閾値k = 8とする.
    # elliptic lagrange test
    # (scalar, elliptic point)
    cnt = 0
    while cnt < 10:
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
            print("elliptic lagrange test: OK")

            
def on_curve_test():
    # 楕円曲線上のランダムな点が曲線状に存在するか確認
    cnt = 0
    while cnt < 10:
        cnt += 1
        H1 = multiply(G1, rnd_scalar())
        if (on_curve(H1)):
            print("True")
        else:
            print("on curve test: NG")
            break
    print("on curve test: OK")

    
def elgamal_test():
    # ElGamal on Elliptic Curve test
    # 楕円エルガマルのテスト(暗号化, 復号)
    cnt = 0
    while cnt < 10:
        cnt += 1
        c = random.randint(10, 50)
        m = rnd_str(c)
        sk, PK = key_generator()
        C1, C2 = encrypt(m, PK)
        r = decrypt(sk, C1, C2)
        if (r == m):
            print(r, "==>", m)
        else:
            print("ElGamal on EC test: NG")
            break
    print("ElGamal on EC test: OK")

    
def ext_field_test():
    # Quadratic extension field test
    # 二次拡大体上での演算のテスト
    # double_G2
    cnt = 0
    while cnt < 10:
        cnt += 1
        if (cnt == 1):
            result = double_G2(G2)
            ref = opt.double(opt.G2)
        else:
            result = double_G2(result)
            ref = opt.double(ref)      
        if (result == FQ2_to_list(ref)):
            print(result, "==>", ref)
        else:
            print("expected", ref, "\nbut got", result)
            break
    print("Doubling on quadratic extension field: OK")
    
    # add_G2
    cnt = 0
    while cnt < 10:
        cnt += 1
        if (cnt == 1):
            result = add_G2(G2, G2)
            ref = opt.add(opt.G2, opt.G2)
        else:
            result = add_G2(G2, result)
            ref = opt.add(opt.G2, ref)
        if (result == FQ2_to_list(ref)):
            print(result, "==>", ref)
        else:
            print("expected", ref, "\nbut got", result)
            break
    print("Add on quadratic extension field: OK")

    # multiply_G2
    cnt = 0
    while cnt < 10:
        cnt += 1
        r = rnd_scalar()
        result = multiply_G2(G2, r)
        ref = opt.multiply(opt.G2, r)
        if (result == FQ2_to_list(ref)):
            print(result, "==>", ref)
        else:
            print("expected", ref, "\nbut got", result)
            break
    print("Multiply on quadratic extension field: OK")

    
def rsa_test():
    cnt = 0
    while cnt < 10:
        cnt += 1
        # 鍵生成 2048 bitで1分強
        sk, pk = rsa.key_generator(256)
        c = random.randint(10, 100)
        m = rnd_str(c)
        print(m)
        c = rsa.encrypt(m, pk)
        res = rsa.decrypt(sk, c)
        if (m == res):
            print(m, "==>", res)
        else:
            print("expected", m, "\nbut got", res)
            exit(1)
    print("RSA test: OK")

    
def miller_rabin_test():
    # miller rabin test
    cnt = 0
    while cnt < 10:
        cnt += 1
        while (True):
            n = rnd_scalar()
            b = rsa.miller_rabin(n, 50)
            if (b):
                break        
        if (sympy.isprime(n)):
            print("prime number: ", n)
        else:
            print("not prime: ", n)
            exit(1)
    print("Miller Rabin test: OK")

    
# homomorphic encryption test for rsa
def rsa_he_test():
    cnt = 0
    while cnt < 10:
        cnt += 1
        m1 = rsa.rnd_scalar(128)
        m2 = rsa.rnd_scalar(128)
        print("m1: ", m1)
        print("m2: ", m2)
        print("m1 * m2: ", m1 * m2)
        r = he.he_rsa(m1, m2)
        if (m1 * m2 == r):
            print(m1 * m2, "==>", r)
        else:
            print("expected", m1 * m2, "\nbut got", r)
            exit(1)
    print("RSA Homomorphic Encryption: OK")

    
# homomorphic encryption test for ElGamal on EC
# FixMe: 復号すると結果が1or2違う場合がある??
def elgamal_he_test():
    cnt = 0
    while cnt < 10:
        cnt += 1
        m1 = secrets.randbits(12)
        m2 = secrets.randbits(12)
        print("m1: ", m1)
        print("m2: ", m2)
        print("m1 * m2: ", m1 * m2)
        r = he.he_elgamal(m1, m2)
        if (m1 * m2 == r):
            print(m1 * m2, "==>", r)
        else:
            print("expected", m1 * m2, "\nbut got", r)
            # 差が1か2でる時がある
            print("sub", r - m1 * m2)
            exit(1)
    print("ElGamal Homomorphic Encryption: OK")


# check calc result using py_ecc optimized bls12-381 library
def main():
    calc_test()
    elliptic_lagrange_test()
    on_curve_test()
    elgamal_test()
    ext_field_test()
    rsa_test()
    miller_rabin_test()
    rsa_he_test()
    elgamal_he_test()
    print("ALL CONFIRMED")


if __name__ == "__main__":
    main()
