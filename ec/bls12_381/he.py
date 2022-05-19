# Homomorphic Encryption
import rsa
import elgamal
import bls12_381

# RSA暗号は乗法準同型暗号の一つ
# RSA is one of Homomorphic Encryption
# m1, m2: message
# c1, c2: encrypted m1, m2
# C: c1 * c2
# decrypted C equals m1 * m2
def he_rsa(m1: int, m2: int) -> int:
    sk, pk = rsa.key_generator(256)
    m = m1 * m2
    # print("m1: ", m1)
    # print("m2: ", m2)
    # print("m1 * m2: ", m)
    c1 = rsa.encrypt(m1, pk)
    c2 = rsa.encrypt(m2, pk)
    # print("c1: ", c1)
    # print("c2: ", c2)
    # print("c1 * c2: ", c1 * c2)
    r1 = rsa.decrypt(sk, c1)
    r2 = rsa.decrypt(sk, c2)
    r = r1 * r2
    return r

# 
# HE for Elgamal on EC
def he_elgamal(m1: int, m2: int) -> int:
    sk, pk = elgamal.key_generator()
    m = m1 * m2
    # c11, c12 = elgamal.encrypt(m1, pk)
    # c21, c22 = elgamal.encrypt(m2, pk)
    C1, C2 = elgamal.encrypt(m, pk)
    r = elgamal.decrypt(sk, C1, C2)
    return r
