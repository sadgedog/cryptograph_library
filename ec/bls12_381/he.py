# Homomorphic Encryption
import rsa


def he_rsa(m1: int, m2: int):
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
