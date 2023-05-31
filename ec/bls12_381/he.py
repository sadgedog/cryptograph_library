# Homomorphic Encryption
import rsa
import elgamal
import paillier
from bls12_381 import (
    add,
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

# RSA暗号は乗法準同型暗号の一つ
# RSA is one of Homomorphic Encryption
# m1, m2: message
# c1, c2: encrypted m1, m2
# C: c1 * c2
# decrypted C equals m1 * m2
def he_rsa(m1: int, m2: int) -> int:
    sk, pk = rsa.key_generator(256)
    c1 = rsa.encrypt(m1, pk)
    c2 = rsa.encrypt(m2, pk)
    C = c1 * c2
    r = rsa.decrypt(sk, C)
    return r


# HE for Elgamal on EC
# Enc(m1) + Enc(m2) = Enc(m1 + m2)
def he_elgamal(m1: int, m2: int) -> int:
    sk, pk = elgamal.key_generator()
    # Enc(m1) + Enc(m2)
    A1, A2 = elgamal.encrypt(m1, pk)
    B1, B2 = elgamal.encrypt(m2, pk)
    D1 = add(A1, B1)
    D2 = add(A2, B2)

    result = elgamal.decrypt(sk, D1, D2)
    i = 0
    while True:
        i += 1
        R = multiply(G1, i)
        if normalize(R) == normalize(result):
            return i
            break


def he_paillier(m1: int, m2: int) -> int:
    sk, pk = paillier.key_generator()
    c1 = paillier.encrypt(m1, pk)
    c2 = paillier.encrypt(m2, pk)
    # Enc(c1) * Enc(c2)
    c = c1 * c2
    r = paillier.decrypt(c, pk, sk)
    return r


#####################################
## this is a test for lifted elgamal
#####################################
## Lifted ElGamal Test: it needs pairing!!
# from py_ecc import optimized_bls12_381 as opt
# G1 = opt.G1
# G2 = opt.G2
# G12 = opt.G12
# pairing = opt.pairing

# def lifted_elgamal(m1: int, m2: int) -> int:
#     sk1 = elgamal.rnd_scalar()
#     pk1 = opt.multiply(G1, sk1)
#     sk2 = elgamal.rnd_scalar()
#     pk2 = opt.multiply(G2, sk2)

#     M1 = opt.multiply(G1, m1)
#     M2 = opt.multiply(G2, m2)

#     r1 = elgamal.rnd_scalar()
#     r2 = elgamal.rnd_scalar()
#     r1G1 = opt.multiply(pk1, r1)
#     r2G2 = opt.multiply(pk2, r2)

#     S1, T1 = opt.add(M1, r1G1), opt.multiply(G1, r1)
#     S2, T2 = opt.add(M2, r2G2), opt.multiply(G2, r2)
#     # a = opt.multiply(G12, (m1 + r1 * sk1) * (m2 + r2 * sk2))
#     # b = opt.multiply(G12, (m1 + r1 * sk1) * r2)
#     # c = opt.multiply(G12, (m2 + r2 * sk2) * r1)
#     # d = opt.multiply(G12, (r1 * r2))
#     # print(a)
#     # print(b)
#     # print(c)
#     # print(d)
#     # D = opt.multiply(d, sk1 * sk2)
#     # B = opt.multiply(b, -sk2)
#     # C = opt.multiply(c, -sk1)
    
#     # FixMe: G12上だと加算ができない（乗算はできる）
#     # MM = opt.add(a, D)
#     # MM = opt.add(MM, B)
#     # MM = opt.add(MM, C)
#     # print(MM)
#     a = pairing(S2, S1)
#     b = pairing(T2, S1)
#     c = pairing(S2, T1)
#     d = pairing(T2, T1)
#     print(a)
