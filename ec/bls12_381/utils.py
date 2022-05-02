# util functions
import time

# time counter 
def time_cnt(func, p):
    s = time.perf_counter()
    func(p, p)
    e = time.perf_counter()
    print(e - s)
