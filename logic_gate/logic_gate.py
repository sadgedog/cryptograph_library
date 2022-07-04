import time

# time counter 
def time_cnt(func, p, q):
    s = time.perf_counter()
    func(p, q)
    e = time.perf_counter()
    print(e - s)

def AND(a: int, b: int):
    if a >= 1 and b >= 1:
        return 1
    else:
        return 0

def NOT(a: int):
    if a >= 1:
        return 0
    else:
        return 1

def OR(a: int, b: int):
    if a >= 1 or b >= 1:
        return 1
    else:
        return 0
 
def NAND(a: int, b: int):
    if a >= 1 and b >= 1:
        return 0
    else:
        return 1

def NOR(a: int, b: int):
    if a <= 0 and b <= 0:
        return 1
    else:
        return 0

def EXOR(a: int, b: int):
    if (a >= 1 and b >= 1) or (a <= 0 and b <= 0):
        return 0
    else:
        return 1
    
def EXNOR(a: int, b: int):
    return NOT(EXOR(a, b))
