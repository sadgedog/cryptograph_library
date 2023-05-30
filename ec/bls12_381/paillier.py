# Paillier cryptosystem
import secrets
import math
from default import co

# p, q is prime number
# N = p * q
# λ = lcm(p-1, q-1)
# μ = (L(g^λ) mod n^2)(-1) mod n(L(u) = (u-1)/n)
# secret key: p, q
# public key: g, n

def rnd_scalar(fm = co) -> int:
    return secrets.randbelow(fm)


# L(u) = (u - 1) / n
def L(u: int, n: int) -> int:
    return (u - 1) // n

    
# [[p, q], [g, n]]
def key_generator() -> list[list[int, int], list[int, int]]:
    p = rnd_scalar()
    q = rnd_scalar()

    while p == q:
        q = rnd_scalar()
    
    n = p * q
    r = math.lcm(p - 1, q - 1)

    g = rnd_scalar(n**2)
    a = L(pow(g, r, n**2), n) % n
    while True:
        g = rnd_scalar(n**2)
        l = L(pow(g, r, n**2), n) % n
        try:
            pow(l, -1, n)
            break
        except ValueError:
            continue

    return [[p, q], [g, n]]



# [[p, q], [g, n]] = key_generator()
# print(p)
# print(q)
# print(g)
# print(n)
