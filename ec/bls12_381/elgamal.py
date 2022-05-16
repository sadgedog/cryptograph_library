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
# separate and encrypt each char
def encrypt(message: str, PK: list):
    M, C2 = list(), list()
    for i in message:
        M.append(message_to_point(i))

    r = rnd_scalar()
    C1 = multiply(G1, r)
    for i in M:
        C2.append(add(i, multiply(PK, r)))
    #print("C1: ", C1)
    #print("C2: ", C2)
    return C1, C2


# Decryption
# M = C2 - xC1
# m = M // 100
# separate and decrypt each char
def decrypt(sk: int, C1: list, C2: list) -> str:
    M, m, r = list(), list(), list()
    result = str()
    for i in range(len(C2)):
        M.append(add(C2[i], negative(multiply(C1, sk))))
        m.append(normalize(M[i])[0] // 100)
        r.append(m[i].to_bytes((m[i].bit_length() + 7) // 8, "big").decode("utf-8"))
        result += r[i]
    print("result", result)
    return result


def message_to_point(message: str) -> list:
    m = int.from_bytes(message.encode("utf-8"), "big") * 100
    for i in range(100):
        x = FE(m + i)
        sqr_y = FE(x**3 + 4)
        if pow(sqr_y, (fm - 1) // 2, fm) == 1:
            return [x, sqr_y, 1]
