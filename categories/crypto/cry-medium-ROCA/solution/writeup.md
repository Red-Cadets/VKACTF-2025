## Решение криптосистемы RSA на основе ROCA-уязвимого ГПСЧ

| Событие | Название | Категория | Сложность |
| :------------- | ----------------------- | ------------------ | ------------------ |
| VKACTF 2025   | Генератор Лаборанта     | crypto             | medium               |

### Описание

> Автор: l1l_w31rd03

Кажется, что Вова испортил алгоритм создания параметров смарт-карт для доступа в Комплекс "Вавилов".

### Решение

Скачиваем cурс-код таска и видим следующую картину: код условно делится на две части: ГПСЧ и RSA.
Разберемся в генераторе: в сурс-коде представлена реализация ГПСЧ, основная задача которого состоит в генерации простых чисел заданной длины для модуля N в RSA. Посмотрим на функцию genPrime:

```python
def genPrime(M, k_size, a_size):
    p = 0
    
    while not isprime(p):
        k = getRandomNBitInteger(k_size)
        a = getRandomNBitInteger(a_size)
        p = k*M + pow(int(65537), a, M)
    return p
```

Видим, что простые числа генерируются на основе формулы: 
$`p = kM + (65537^a) \bmod M`$
где M - мультипликативная группа порядка n, то есть результат умножения n простых чисел, рассчитываемая по длине ключа, параметры a и k - также неизвестны и генерируются на основе длины ключа:

```python
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
        print("Invalid key size.")
        return None
    M = primorial(n)
    k_size = keySize // 2 - round(log(M, 2))
    a_size = ceil(log(n_order(65537, M), 2))
    return M, k_size, a_size
```

Проведя небольшой анализ и поискав информацию в интернете, можем узнать, что это реализация ROCA-уязвимого ГПСЧ (аналог ГПСЧ, использовавшегося в RSAlib, CVE 2017-153610).
Следовательно, нам необходимо провести атаку ROCA (акроним для Return of Coppersmith's Attack), которая заключается в факторизации модуля n в RSA. Для этого мы можем воспользоваться атакой типа ```coppersmith_howgrave_univariate```, реализацию которой мы можем легко найти на гитхабе. 
Далее, для факторизации n, необходимо найти параметр a, что является тривиальной задачей, заключающейся, по факту, в реализации алгоритма Полига-Хелмана, для упрощения имплементации воспользуемся ЯП Sage:

```Sage
def isVuln(n):
    params = getParameterSizes(n.bit_length())
    if params is not None:
        M = params[0]
        a = Zmod(M)(n).log(65537)
        return a
```
Данная функция основана на дискретном логарифмировании в кольце вычетов по модулю простого числа, где простым числом является M (так как является мультипликативной группой).
Восстановив значение a, переходим к эскплуатации алгоритма CHG (Coppersmith HowGrave):

```Sage
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
```

И, наконец-таки опишем саму атаку ROCA:

```Sage
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
```
Здесь мы используем уже известное нам значение M, так как keysize в сурс-коде определяется, как 512 бит, также для ускорения вычислений применим multiprocessing, что сократит его (даже для достаточно слабых конфигураций) до ~8-10 минут (для еще большего ускорения можно переписать код под CUDA).
После нахождения разложения модуля N на простые p, q, решить RSA не явлется трудной задачей).

```Python
def RSA_decrypt(n, p, q, e, ct):
    
    phi = (p - 1) * (q - 1)
    
    d = pow(e, -1, phi)
    pt = pow(ct, d, n)
    
    flag = long_to_bytes(pt).decode()
    
    print(f"ФЛАГ: {flag}")
```
Полное решение написано на ЯП Sage - [solution.py](./solution.py)

Флаг

```
vka{it_seems_that_rng_is_broken}
```
