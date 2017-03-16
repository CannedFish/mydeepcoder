# -*- coding: utf-8 -*-

# 0 -> int, 1 -> [int], 2 -> bool, 3 -> lambda(int), 4 -> lambda(int, int)
TYPE = ['int', '[int]', 'bool']

# [func, input type, output type]
# First Order
First_Order = {
    'HEAD': [lambda v: v[0] if len(v)>0 else None, (1,), 0],
    'LAST': [lambda v: v[-1] if len(v)>0 else None, (1,), 0],
    'TAKE': [lambda n, v: v[:n], (0, 1), 1],
    'DROP': [lambda n, v: v[n:], (0, 1), 1],
    'ACCESS': [lambda n, v: v[n] if n>=0 and len(v)>n else None, (0, 1), 1],
    'MINIMUM': [lambda v: min(v) if len(v)>0 else None, (1,), 0],
    'MAXIMUM': [lambda v: max(v) if len(v)>0 else None, (1,), 0],
    'REVERSE': [lambda v: list(reversed(v)), (1,), 1],
    'SORT': [lambda v: sorted(v), (1,), 1],
    'SUM': [lambda v: sum(v), (1,), 1],
}
 
def SCANL1(f, v):
    if len(v) > 0:
        y = [v[0]] * len(v)
        for i in range(1, len(v)):
            y[i] = f(y[i-1], v[i])
        return y
    else:
        return None

# High Order
High_Order = {
    'MAP': [lambda f, v: [f(x) for x in v], (3, 1), 1],
    'FILTER': [lambda f, v: [x for x in v if f(x)], (3, 1), 1],
    'COUNT': [lambda f, v: len([x for x in v if f(x)]), (3, 1), 1],
    'ZIPWITH': [lambda f, v1, v2: [f(x, y) for x, y in zip(v1, v2)], (4, 1, 1), 1],
    'SCANL1': [SCANL1, (4, 1), 1]
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
    '(>0)': [lambda x: x>0, (0,), 0, 3],
    '(<0)': [lambda x: x<0, (0,), 0, 3],
    '(%2==0)': [lambda x: x%2==0, (0,), 0, 3],
    '(%2==1)': [lambda x: x%2==1, (0,), 0, 3],
    '(+)': [lambda x, y: x+y, (0, 0), 0, 4],
    '(-)': [lambda x, y: x-y, (0, 0), 0, 4],
    '(*)': [lambda x, y, x*y, (0, 0), 0, 4],
    'MIN': [lambda x, y: x if x<y else y, (0, 0), 0, 4],
    'MAX': [lambda x, y: x if x>y else y, (0, 0), 0, 4],
}

