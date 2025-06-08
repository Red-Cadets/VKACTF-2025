from sage.all import *
from Crypto.Util.number import long_to_bytes

def primorial(n):
    M = 1
    p = 1
    for i in range(n):
        p = next_prime(p)
        M *= p
    return int(M)


def getParameterSizes(keySize):
    if 512 <= keySize <= 960:
        n = 39
    elif 992 <= keySize <= 1952:
        n = 71
    elif 1984 <= keySize <= 3936:
        n = 126
    elif 3968 <= keySize <= 4096:
        n = 225
    else:
        print("Неправильный размер ключа.")
        return None
    M = primorial(n)
    k_size = keySize//2 - round(log(M, 2))
    a_size = ceil(log(Zmod(M)(65537).multiplicative_order(), 2))
    return M, k_size, a_size


def isVuln(n):
    params = getParameterSizes(n.bit_length())
    if params is not None:
        M = params[0]
        a = Zmod(M)(n).log(65537)
        return a


def solve(M, n, a, m):
    from coppersmith import coppersmith_howgrave_univariate

    base = int(65537)
    known = int(pow(base, a, M) * inverse_mod(M, n))
    F = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    (x,) = F._first_ngens(1)
    pol = x + known
    beta = 0.1
    t = m+1
    XX = floor(2 * n**0.5 / M)
    roots = coppersmith_howgrave_univariate(pol, n, beta, m, t, XX)
    for k in roots:
        p = int(k*M + pow(base, a, M))
        if n%p == 0:
            return p, n//p


def roca(n):
    keySize = n.bit_length()
    
    if keySize <= 960:
        M_prime = 0x1b3e6c9433a7735fa5fc479ffe4027e13bea
        m = 5

    else:
        print("Неправильный размер ключа: {}".format(keySize))
        return None

    a3 = Zmod(M_prime)(n).log(65537)
    order = Zmod(M_prime)(65537).multiplicative_order()
    inf = a3 // 2
    sup = (a3 + order) // 2

    chunk_size = 10000
    for inf_a in range(inf, sup, chunk_size):
        inputs = [((M_prime, n, a, m), {}) for a in range(inf_a, inf_a+chunk_size)]
        from sage.parallel.multiprocessing_sage import parallel_iter
        from multiprocessing import cpu_count

        for k, val in parallel_iter(cpu_count(), solve, inputs):
            if val:
                p = val[0]
                q = val[1]
                print("Факторизовано:\np = {}\nq = {}".format(p, q))
                return val
            
            
def RSA_decrypt(n, p, q, e, ct):
    
    phi = (p - 1) * (q - 1)
    
    d = pow(e, -1, phi)
    pt = pow(ct, d, n)
    
    flag = long_to_bytes(pt).decode()
    
    print(f"ФЛАГ: {flag}")
    

if __name__ == "__main__":
    
    n = int(input("Введите n: "))
    
    a = isVuln(n)
    p, q = roca(n)
    
    e = int(input("Введите e: "))
    ct = int(input("Введите ct: "))
    
    RSA_decrypt(n, p, q, e, ct)