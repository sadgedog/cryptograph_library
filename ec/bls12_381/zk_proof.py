import sys
import hashlib
from utils import (
    rnd_scalar,
)
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
    normalize,
)


def zk_proof(message: int, G1_point: list) -> list:
    w = rnd_scalar()
    T = multiply(G1, w)
    T = normalize(T)
    value = G1 + G1_point + T
    tmp = 0
    for i in value:
        tmp += i
    tmp = hex(tmp).encode()
    
    challenge = hashlib.sha256(tmp).hexdigest()
    challenge = int(challenge, 16)
    response = (w - message * challenge) % co
        
    return [challenge, response]


def verify_zk_proof(G1_point, c, r) -> bool:
    A = multiply(G1, r)
    B = multiply(G1_point, c)
    T = add(A, B)
    T = normalize(T)
    value = G1 + G1_point + T
    tmp = 0
    for i in value:
        tmp += i
    
    tmp = hex(tmp).encode()
    verified_challenge = hashlib.sha256(tmp).hexdigest()
    verified_challenge = int(verified_challenge, 16)

    return [c, verified_challenge]
