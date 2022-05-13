import math
import secrets

# RSA Encryption

def key_generator(i: int):
    p = q = 0
    while (p == q):
        p, q = 6733, 9973
        #p, q = 965411, 719167
    n = p * q
    phi = math.lcm(p-1, q-1)

    # TODO: 全探索以外のアルゴリズム
    for i in range(2, phi):
        if math.gcd(i, phi) == 1:
            e = i
            break
        
    for i in range(2, phi):
        if (e * i) % phi == 1:
            d = i
            break
    return [d, n], [e, n]


def rnd_scalar(i: int):
    return secrets.randbits(i)

# separate and encrypt each char
def encrypt(message: str, pk: list):
    l = list()
    for i in range(len(message)):
        l.append(int.from_bytes(message[i].encode("utf-8"), "big"))
    #l = [ord(char) for char in message]
    
    # m = int.from_bytes(message.encode("utf-8"), "big")
    # print("m:", m)
    e = pk[0]
    n = pk[1]
    c = [pow(i, e, n) for i in l]
    return c

def decrypt(sk: list, c: list):
    d = sk[0]
    n = sk[1]
    # decrypt
    m = [pow(i, d, n) for i in c]
    # decode 
    m = [i.to_bytes((i.bit_length() + 7) // 8, "big").decode("utf-8") for i in m]
    r = ""
    for i in range(len(m)):
        r += m[i]        
    return r


# TODO: miller_rabinの素数判定アルゴリズムでランダムな素数を作る
def miller_rabin_rnd():
    return 0
