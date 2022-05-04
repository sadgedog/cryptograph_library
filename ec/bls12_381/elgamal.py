import secrets
from default import (
    co,
    fm,
    G1,
    G2,
    Z1,
    Z2,
)
from bls12_381 import (
    add,
    multiply,
    FE,
    normalize,
    on_curve,
    negative,
)

# ElGamal on Elliptic Curve

def rnd_scalar():
    return secrets.randbelow(co)

def key_generator():
    # secret key: sk = random
    sk = rnd_scalar()
    # Public Key: PK = sk*G1
    PK = multiply(G1, sk)
    print("sk: ", sk)
    print("PK: ", PK)
    return sk, PK

# Encryption:
# M <- message to point
# r <- random scalar
# cipher text C1, C2
# C1 <- rG1
# C2 <- M + rPK
def encrypt(message: str, PK: list):
    M = message_to_point(message)
    print("M: ", M[0])
    r = rnd_scalar()
    C1 = multiply(G1, r)
    C2 = add(M, multiply(PK, r))
    print("C1: ", C1)
    print("C2: ", C2)
    return [C1, C2]

# Decryption
# M = C2 - xC1
# m = M // 100
def decrypt(sk: int, C1: list, C2: list) -> str:
    M = add(C2, negative(multiply(C1, sk)))
    m = normalize(M)[0] // 100
    result = m.to_bytes((m.bit_length() + 7) // 8, "big").decode("utf-8")
    return result
    
def message_to_point(message: str) -> list:
    m = int.from_bytes(message.encode("utf-8"), "big") * 100
    for i in range(100):
        x = FE(m + i)
        sqr_y = FE(x**3 + 4)
        if (pow(sqr_y, (fm - 1) // 2, fm) == 1):
            return [x, sqr_y, 1]
