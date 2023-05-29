import numpy as np
import numpy.linalg as LA

#
# GSW暗号
# 秘密鍵s: 固有ベクトルv
# 固有値w: 平文m
# 暗号文c: 行列A
# エラーe
# Av = wv + e


def gen_secret_key(message: int):
    pass

def bit_decomp(a: np.array, L: int, k: int) -> np.array:
    pass

def bit_decomp_inv(a: np.array, L: int, k: int) -> np.array:
    pass

def flatten(a: np.array, L: int, k: int) -> np.array:
    return bit_decomp(bit_decomp_inv(a, L, k), L, k);


def calc_eigen():
    A = np.array([[1, 0], [0, 2]])
    w, v = LA.eig(A)

    
calc_eigen()
