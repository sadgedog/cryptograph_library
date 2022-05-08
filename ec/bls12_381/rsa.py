import math
import secrets

# RSA Encryption

def key_generator(i: int):
    p = q = 0
    while (p == q):
        # TODO: miller rabinの素数判定でランダムな素数を作る
        p, q = 6733, 9973

    print("p, q: ", p, "\n", q)
    n = p * q
    print("n: ", n)
    phi = math.lcm(p-1, q-1)
    print("phi: ", phi)
    
    for i in range(2, phi):
        if math.gcd(i, phi) == 1:
            e = i
            break
    print("e: ", e)
    for i in range(2, phi):
        if (e * i) % phi == 1:
            d = i
            break
    print("d: ", d)
    return [d, n], [e, n]


def rnd_scalar(i: int):
    return secrets.randbits(i)

def encrypt(message: int, pk: list):
    e = pk[0]
    n = pk[1]
    c = pow(message, e, n)
    return c

def decrypt(sk: list, c: int):
    d = sk[0]
    n = sk[1]
    m = pow(c, d, n)
    return m

sk, pk = key_generator(10)
print("sk: ", sk)
print("pk: ", pk)
c = encrypt(1254, pk)
print("c: ", c)

m = decrypt(sk, c)
print("m: ", m)
