# Paillier cryptosystem
import secrets
import math
import random
from default import co

from Crypto.Util import number

# p, q is prime number
# N = p * q
# λ = lcm(p-1, q-1)
# μ = (L(g^λ) mod n^2)(-1) mod n(L(u) = (u-1)/n)
# secret key: p, q
# public key: g, n

def rnd_scalar(fm = co) -> int:
    return secrets.randbelow(fm)



def miller_rabin(p: int, k: int = 100) -> bool:
    if p == 1 or p & 1 == 0:
        return False
    elif p == 2:
        return True
    
    d = (p - 1) // 2
    while d & 1 == 0:
        d = d // 2
        
    for i in range(k):
        a = random.randint(1, p - 1)
        t = d
        y = pow(a, t, p)
        
        while t != p - 1 and y != 1 and y != p - 1:
            y = (y * y) % p
            t = t * 2
        if y != p - 1 and t & 1 == 0:
            return False
    return True


# L(u) = (u - 1) / n
def L(u: int, n: int) -> int:
    return (u - 1) // n

    
# [sk, pk]
def key_generator() -> list[list[int, int], list[int, int]]:
    # p, q: prime number 
    p = rnd_scalar()
    q = rnd_scalar()
    while not miller_rabin(p):
        p = rnd_scalar()
        if miller_rabin(p):
            break

    while not miller_rabin(q):
        q = rnd_scalar()
        if miller_rabin(q):
            break

    while p == q:
        q = rnd_scalar()
    
    n = p * q
    r = math.lcm(p - 1, q - 1)

    g = number.getRandomRange(2, n*n)
    while True:
        g = number.getRandomRange(2, n*n)
        l = L(pow(g, r, n**2), n) % n
        try:
            u = pow(l, -1, n)
            break
        except ValueError:
            continue

    return [[r, u], [g, n]]


# c = g^m * r^n mod(n^2)
def encrypt(m: int, pk: list[int, int]) -> int:
    g, n = pk
    while True:
        r = rnd_scalar(n)
        if math.gcd(r, n) == 1:
            break
    c = (pow(g, m, n**2) * pow(r, n, n**2)) % n**2
    
    return c


def decrypt(c: int, pk: list[int, int], sk: list[int, int]) -> int:
    g, n = pk
    r, u = sk
    m = (L(pow(c, r, n**2), n) * u) % n
    return m
