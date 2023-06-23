import secrets

# random element over torus
def rnd_torus(bit_length: int = 64) -> float:
    rnd = secrets.randbits(bit_length)
    rnd_torus = rnd / (1 << bit_length)
    return rnd_torus


# T(X) = μ  μ + μX^2+ ... + μX
def torus_polynomial(X: float, n: int, mu: float) -> float:
    result = 0.0;
    exponent = 1.0
    for _ in range(n):
        result += mu * exponent
        exponent *= X
        
    return result % 1.0
