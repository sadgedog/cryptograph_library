# Paillier cryptosystem
import secrets
from math import lcm
from default import co

# p, q is prime number
# N = p * q
# λ = lcm(p-1, q-1)
# μ = (L(g^λ) mod n^2)(-1) mod n(L(u) = (u-1)/n)
# secret key: p, q
# public key: g, n

def rnd_scalar() -> int:
    return secrets.randbelow(co)


def helper_key_generator(u: int, n: int) -> int:
    return (u - 1) // n


def key_generator() -> list[list[int, int], list[int, int]]:
    p = rnd_scalar()
    q = rnd_scalar()

    while p == q:
        q = rnd_scalar()
    
    n = p * q
    r = lcm(p - 1, q - 1)
