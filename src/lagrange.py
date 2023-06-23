from fractions import Fraction
import sympy
import secrets
import hashlib
from default import (
    co,
    G1,
    G2,
    Z1,
    Z2,
)
from bls12_381 import (
    add,
    multiply,
)


# lagrange interpolation in elliptic curve
def elliptic_lagrange(x: int, point: list, p: str) -> int:
    x_point, y_point = list(), list()
    # Z1: additive identity element
    if p == "Z1":
        result = Z1
    elif p == "Z2":
        result = Z2
    for i in range(len(point)):
        x_point.append(point[i][0])
        # y_point: point on elliptic curve ([X : Y : Z])
        y_point.append(point[i][1])
    for i in range(len(point)):
        elc = elliptic_lagrange_coef(x, i, len(x_point), x_point)
        mul = multiply(y_point[i], elc)
        result = add(result, mul)        
    return result


def elliptic_lagrange_coef(x: int, i: int, a: int, x_point: list) -> int:
    result = 1
    for j in range(a):
        if i != j:
            result *= Fraction(x - x_point[j], x_point[i] - x_point[j])
    return int(result)


def rnd_scalar() -> int:
    return secrets.randbelow(co)


def hash_to_scalar(msg) -> int:
    return (
        int.from_bytes(hashlib.sha3_256(str(msg).encode()).digest(), "big")
        % co
    )


def generate_share(secret: int, n: int, t: int) -> list[list, list]:
    coefficients = [secret] + [hash_to_scalar(f"vss:coefficient:{secret}:{j}") for j in range(1, t)]

    def f(x):
        func = sum(coef * pow(x, j, co) for j, coef in enumerate(coefficients)) % co
        return func
    
    shares = [f(id) for id in range(1, n + 1)]
    public_coefficients = [multiply(G1, coef) for coef in coefficients]
    return [shares, public_coefficients]
