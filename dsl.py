# -*- coding: utf-8 -*-

import random, math

def SCANL1(f, v):
    if len(v) > 0:
        y = [v[0]] * len(v)
        for i in range(1, len(v)):
            y[i] = f(y[i-1], v[i])
        return y
    else:
        return None

# 0 -> int, 1 -> [int], 2 -> bool, 3 -> lambda(int), 4 -> lambda(int, int)
TYPE = ['int', '[int]', 'bool']

# [func, input type, output type]
FUNCs = {
# First Order
    'FO': {
        'HEAD': [lambda v: v[0] if len(v)>0 else None, (1,), 0],
        'LAST': [lambda v: v[-1] if len(v)>0 else None, (1,), 0],
        'TAKE': [lambda n, v: v[:n], (0, 1), 1],
        'DROP': [lambda n, v: v[n:], (0, 1), 1],
        'ACCESS': [lambda n, v: v[n] if n>=0 and len(v)>n else None, (0, 1), 1],
        'MINIMUM': [lambda v: min(v) if len(v)>0 else None, (1,), 0],
        'MAXIMUM': [lambda v: max(v) if len(v)>0 else None, (1,), 0],
        'REVERSE': [lambda v: list(reversed(v)), (1,), 1],
        'SORT': [lambda v: sorted(v), (1,), 1],
        'SUM': [lambda v: sum(v), (1,), 0],
    },
# High Order
    'HO': {
        'MAP': [lambda f, v: [f(x) for x in v], (3, 1), 1],
        'FILTER': [lambda f, v: [x for x in v if f(x)], (3, 1), 1],
        'COUNT': [lambda f, v: len([x for x in v if f(x)]), (3, 1), 0],
        'ZIPWITH': [lambda f, v1, v2: [f(x, y) for x, y in zip(v1, v2)], (4, 1, 1), 1],
        'SCANL1': [SCANL1, (4, 1), 1]
    }
}

# [lambda, input type, output type, lambda type]
# Lambdas
Lambdas = {
    '(+1)': [lambda x: x+1, (0,), 0, 3],
    '(-1)': [lambda x: x-1, (0,), 0, 3],
    '(*2)': [lambda x: x*2, (0,), 0, 3],
    '(/2)': [lambda x: x/2, (0,), 0, 3],
    '(*(-1))': [lambda x: x*(-1), (0,), 0, 3],
    '(**2)': [lambda x: x**2, (0,), 0, 3],
    '(*3)': [lambda x: x*3, (0,), 0, 3],
    '(/3)': [lambda x: x/3, (0,), 0, 3],
    '(*4)': [lambda x: x*4, (0,), 0, 3],
    '(/4)': [lambda x: x/4, (0,), 0, 3],
    '(>0)': [lambda x: x>0, (0,), 2, 3],
    '(<0)': [lambda x: x<0, (0,), 2, 3],
    '(%2==0)': [lambda x: x%2==0, (0,), 2, 3],
    '(%2==1)': [lambda x: x%2==1, (0,), 2, 3],
    '(+)': [lambda x, y: x+y, (0, 0), 0, 4],
    '(-)': [lambda x, y: x-y, (0, 0), 0, 4],
    '(*)': [lambda x, y: x*y, (0, 0), 0, 4],
    'MIN': [lambda x, y: x if x<y else y, (0, 0), 0, 4],
    'MAX': [lambda x, y: x if x>y else y, (0, 0), 0, 4],
}

def _gen_ordered_list(min_=None, max_=None, length=None):
    l = length-1 if length is not None \
            else random.randint(5, 10)
    if min_ is not None and max_ is None:
        start = min_
        end = start + l
    elif max_ is not None and min_ is None:
        end = max_
        start = end - l
    elif max_ is not None and min_ is not None:
        start = min_
        end = max_
    else:
        start = random.randint(-10, 10)
        end = start + l
    return range(start, end+1)

def _gen_list(min_=None, max_=None):
    if min_ is not None and max_ is None:
        low_end = min_
        high_end = min_ + 20
    elif min_ is None and max_ is not None:
        high_end = max_
        low_end = max_ - 20
    elif min_ is not None and max_ is not None:
        if min_ >= max_:
            raise ValueError('max_ must bigger than min_')
        low_end = min_
        high_end = max_
    else:
        low_end = -10
        high_end = 10

    length = random.randint(5, 10)
    gen_list = [random.randint(low_end-1, high_end-1) \
            for i in xrange(length)]
    gen_list[random.randint(0, len(gen_list)-1)] = low_end \
            if min_ is not None else high_end
    return gen_list

def ReHEAD(n, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(min_=n/gcd) \
            if ordered else _gen_list()
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    gen_list[0] = n
    return gen_list

def ReLAST(n, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(max_=n/gcd) \
            if ordered else _gen_list()
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    gen_list[-1] = n
    return gen_list

def ReTAKE(v, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(min_=v[-1]/gcd) \
            if ordered else _gen_list()
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    return len(v), v + gen_list[1:]

def ReDROP(v, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(max_=v[0]/gcd) \
            if ordered else _gen_list()
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    return len(gen_list)-1, gen_list[:-1] + v

def ReACCESS(n, gcd=1, ordered=False):
    if ordered:
        gen_list1 = _gen_ordered_list(max_=n/gcd, \
                length=random.randint(2, 5))
        gen_list2 = _gen_ordered_list(min_=n/gcd, \
                length=random.randint(2, 5))
        idx, gen_list = len(gen_list1)-1, gen_list1+gen_list2[1:]
    else:
        gen_list = _gen_list()
        idx = random.randint(0, len(gen_list)-1)
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    gen_list[idx] = n
    return idx, gen_list

def ReMINIMUM(n, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(min_=n/gcd) \
            if ordered else _gen_list(min_=n/gcd)
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    return gen_list

def ReMAXIMUM(n, gcd=1, ordered=False):
    gen_list = _gen_ordered_list(max_=n/gcd) \
            if ordered else _gen_list(max_=n/gcd)
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    return gen_list

def ReSORT(v):
    random.shuffle(v)
    return v

def ReSUM(n, gcd=1, ordered=False):
    gen_list = []
    n /= gcd
    negative = False
    if n < 0:
        n = -n
        negative = True
    for i in xrange(n):
        if i <= n:
            gen_list.append(i)
            n -= i
        else:
            break
    gen_list.append(n)
    if negative:
        gen_list = map(lambda x: -x, gen_list)
    for i in xrange(2):
        x = random.randint(-10, 10)
        gen_list.extend([x, -x])
    if gcd != 1:
        gen_list = map(lambda x: x*gcd, gen_list)
    if ordered:
        gen_list = sorted(gen_list)
    else:
        random.shuffle(gen_list)
    return gen_list

def ReFilter_p():
    pass

def ReFilter_n():
    pass

def ReFilter_even():
    pass

def ReFilter_odd():
    pass

ReFUNCs = {
    'FO': {
        'HEAD': ReHEAD,
        'LAST': ReLAST,
        'TAKE': ReTAKE,
        'DROP': ReDROP,
        'ACCESS': ReACCESS,
        'MINIMUM': ReMINIMUM,
        'MAXIMUM': ReMAXIMUM,
        'REVERSE': lambda v: list(reversed(v)),
        'SORT': ReSORT,
        'SUM': ReSUM
    },
    'HO': {
        'FILTER_(>0)': ReFilter_p,
        'FILTER_(<0)': ReFilter_n,
        'FILTER_(%2==0)': ReFilter_even,
        'FILTER_(%2==1)': ReFilter_odd,
    }
}

def ReLambda_add(n, gcd=1):
    n /= gcd
    a = random.randint(n-20, n)
    b = n - a
    if gcd > 1:
        a *= gcd
        b *= gcd
    return a, b

def ReLambda_del(n, gcd=1):
    n /= gcd
    a = random.randint(-10, 10)
    b = n + a
    if gcd > 1:
        a *= gcd
        b *= gcd
    return b, a

def ReLambda_mul(n, gcd=1):
    n /= gcd
    while True:
        a = random.randint(1, 10)
        if n%a == 0:
            break
    b = n / a
    if gcd > 1:
        b *= gcd
    return a, b

def ReLambda_min(n, gcd=1):
    return (n + random.randint(0, 5)) * gcd, n

def ReLambda_max(n, gcd=1):
    return (n - random.randint(0, 5)) * gcd, n

ReLambdas = {
    '(+1)': lambda x: x-1,
    '(-1)': lambda x: x+1,
    '(*2)': lambda x: x/2,
    '(/2)': lambda x: x*2,
    '(*(-1))': lambda x: x*(-1),
    '(**2)': lambda x: int(math.sqrt(x)),
    '(*3)': lambda x: x/3,
    '(/3)': lambda x: x*3,
    '(*4)': lambda x: x/4,
    '(/4)': lambda x: x*4,
    # '(>0)': [lambda x: x>0, (0,), 2, 3],
    # '(<0)': [lambda x: x<0, (0,), 2, 3],
    # '(%2==0)': [lambda x: x%2==0, (0,), 2, 3],
    # '(%2==1)': [lambda x: x%2==1, (0,), 2, 3],
    '(+)': ReLambda_add,
    '(-)': ReLambda_del,
    '(*)': ReLambda_mul,
    'MIN': ReLambda_min,
    'MAX': ReLambda_max,
}

