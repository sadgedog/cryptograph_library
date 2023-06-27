import secrets
import numpy as np
from utils import (
    scaling,
)
from torus import (
    rnd_torus
)

# security parameter for 128bits security strength
# n = 630
# sigma = 2 ** (-15)

# p = 1024

# secret key: sk_tlwe = (s_1, s_2, ... ,s_n) ∈ Bn {0, 1}
def key_generator(n: int) -> np.array:
    return np.array([secrets.randbits(1) for i in range(n)], dtype=np.uint64)


# modulo gausiaan distribution
def modulo_gaussian(ave: float, sigma: float, size: int = 1) -> float:
    return np.random.normal(ave, sigma, size) % 1


# a = N(mu, sigma)
# b = sum(s_j * a_j) + e + mu
# c = (a, b)
def tlwe_encrypt(sk: np.array, mu: float, sigma: float) -> np.array:
    a = np.array([rnd_torus(64) for _ in range(len(sk))], dtype=np.float64)
    b = np.dot(a, sk) +  modulo_gaussian(0, sigma, 1)[0] + mu
    c = np.append(a, b)
    return c


# mu = (⌊p * mu_aster⌉ mod p / 2p)
def tlwe_decrypt(sk: np.array, c: np.array, p: int) -> float:
    b = c[-1]
    a = c[0:-1]
    mu_aster = b - np.dot(sk, a)
    mu = (scaling(p * mu_aster) % p) / p
    return mu


# {0, 1} -> [0, 1)
def binary_encoder(mu: int) -> float:
    return mu / 2


# [0, 1) -> {0, 1}
def binary_decoder(dec: float) -> int:
    return scaling(2 * dec) % 2


# {0, ... , p-1} -> [0, 1)
def integer_encoder(mu: int, p: int) -> float:
    return (mu % p) / p


# [0, 1) -> {0, ... , p-1}
def integer_decoder(dec: float, p: int) -> int:
    return scaling(p * dec) % p
