import math
import random
import secrets

# RSA Encryption

def key_generator(bitlen: int) -> list:
    p = q = 0
    p = rnd_scalar(bitlen)
    q = rnd_scalar(bitlen)
    while (not miller_rabin(p)):
        p = rnd_scalar(bitlen)
        if (miller_rabin(p)):
            break

    while (not miller_rabin(q)):
        q = rnd_scalar(bitlen)
        if (miller_rabin(q)):
            break
        
    n = p * q
    phi = math.lcm(p-1, q-1)

    for i in range(2, phi):
        if math.gcd(i, phi) == 1:
            e = i
            break
    d = ext_gcd(e, phi)
    return [d, n], [e, n]


def rnd_scalar(i: int) -> int:
    return secrets.randbits(i)

# separate and encrypt each char
def encrypt(message: str or int, pk: list) -> list or int:
    # string
    if (type(message) == str):
        enc_l = list()
        for i in range(len(message)):
            enc_l.append(int.from_bytes(message[i].encode("utf-8"), "big"))
        e = pk[0]
        n = pk[1]
        c = [pow(i, e, n) for i in enc_l]
    # integer
    elif (type(message) == int):
        e = pk[0]
        n = pk[1]
        c = pow(message, e, n)
        
    return c

def decrypt(sk: list, c: list or int) -> str or int:
    d = sk[0]
    n = sk[1]
    # string
    if (type(c) == list):
        # decrypt
        m = [pow(i, d, n) for i in c]
        # decode
        m = [i.to_bytes((i.bit_length() + 7) // 8, "big").decode("utf-8") for i in m]
        r = ""
        for i in range(len(m)):
            r += m[i]
    # integer
    elif (type(c) == int):
        r = pow(c, d, n)
        
    return r


def miller_rabin(p: int, k: int = 100) -> bool:
    if (p == 1 or p & 1 == 0):
        return False
    elif (p == 2):
        return True
    
    d = (p - 1) // 2
    while (d & 1 == 0):
        d = d // 2

    for i in range(k):
        a = random.randint(1, p - 1)
        t = d
        y = pow(a, t, p)
        
        while (t != p - 1 and y != 1 and y != p - 1):
            y = (y * y) % p
            t = t * 2
        if (y != p - 1 and t & 1 == 0):
            return False
    return True

# extended gcd
# a * x + b * y = 1
def ext_gcd(a: int, b: int) -> int:
    h = b
    x, y, u, v = 1, 0, 0, 1
    while b:
        k = a // b
        x -= k * u
        y -= k * v
        x, u = u, x
        y, v = v, y
        a, b = b, a % b
    x %= h
    if x < 0:
        x += h
    return x
