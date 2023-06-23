import secrets
import numpy as np
from utils import (
    scaling,
)
from torus import (
    rnd_torus
)

# security parameter for 128bits security strength
n = 630
sigma = 2 ** (-15)

# p : OK?
p = 1024

# secret key: sk_tlwe = (s_1, s_2, ... ,s_n) ∈ Bn {0, 1}
def key_generator(n: int) -> np.array:
    return np.array([secrets.randbits(1) for i in range(n)], dtype=np.uint64)


# modulo gausiaan distribution
def modulo_gaussian(mu: float, sigma: float, size: int = 1) -> float:
    return np.random.normal(mu, sigma, size) % 1


# a = N(mu, sigma)
# b = sigma(s_j * a_j) + e + mu
# c = (a, b)
def tlwe_encrypt(sk: np.array, mu: float, sigma: float) -> np.array:
    a = np.array([rnd_torus(32) for _ in range(len(sk))], dtype=np.float64)
    b = np.dot(a, sk) + modulo_gaussian(mu, sigma, 1)[0] + mu
    c = np.append(a, b)
    return c


# mu = (⌊p * mu_aster⌉ mod p / p)
def tlwe_decrypt(sk: np.array, c: np.array, p: int) -> float:
    b = c[-1]
    a = c[0:-1]
    mu_aster = b - np.dot(sk, a)
    mu = (scaling(p * mu_aster) % p) / (p * 2)
    return mu
