# -*- coding=utf-8 -*-

import random
from dsl import FUNCs, Lambdas, ReFUNCs, ReLambdas

vector = [4, -10, 3, 7, -9, 2, -1, -2]
ordered_vector = range(-4, 4)
value = 3

def head_test():
    ret = FUNCs['FO']['HEAD'][0](vector)
    print '%s, %d, %s' % (vector, ret, ReFUNCs['FO']['HEAD'](ret))
    ret = FUNCs['FO']['HEAD'][0](ordered_vector)
    print '%s, %d, %s' % (ordered_vector, ret, ReFUNCs['FO']['HEAD'](ret, gcd=2, ordered=True))

def last_test():
    ret = FUNCs['FO']['LAST'][0](vector)
    print '%s, %d, %s' % (vector, ret, ReFUNCs['FO']['LAST'](ret))
    ret = FUNCs['FO']['LAST'][0](ordered_vector)
    print '%s, %d, %s' % (ordered_vector, ret, ReFUNCs['FO']['LAST'](ret, gcd=3, ordered=True))

def take_test():
    ret = FUNCs['FO']['TAKE'][0](value, vector)
    print '%s, %s, %s' % (vector, ret, ReFUNCs['FO']['TAKE'](ret))
    ret = FUNCs['FO']['TAKE'][0](value, ordered_vector)
    print '%s, %s, %s' % (ordered_vector, ret, ReFUNCs['FO']['TAKE'](ret, gcd=2, ordered=True))

def drop_test():
    ret = FUNCs['FO']['DROP'][0](value, vector)
    print '%s, %s, %s' % (vector, ret, ReFUNCs['FO']['DROP'](ret))
    ret = FUNCs['FO']['DROP'][0](value, ordered_vector)
    print '%s, %s, %s' % (ordered_vector, ret, ReFUNCs['FO']['DROP'](ret, gcd=2, ordered=True))

def access_test():
    ret = FUNCs['FO']['ACCESS'][0](value, vector)
    print '(%d, %s), %d, %s' % (value, vector, ret, ReFUNCs['FO']['ACCESS'](ret))
    ret = FUNCs['FO']['ACCESS'][0](value, ordered_vector)
    print '(%d, %s), %d, %s' % (value, ordered_vector, ret, ReFUNCs['FO']['ACCESS'](ret, gcd=2, ordered=True))

def minimum_test():
    ret = FUNCs['FO']['MINIMUM'][0](vector)
    print '%s, %d, %s' % (vector, ret, ReFUNCs['FO']['MINIMUM'](ret))
    ret = FUNCs['FO']['MINIMUM'][0](ordered_vector)
    print '%s, %d, %s' % (ordered_vector, ret, ReFUNCs['FO']['MINIMUM'](ret, gcd=2, ordered=True))

def maximum_test():
    ret = FUNCs['FO']['MAXIMUM'][0](vector)
    print '%s, %d, %s' % (vector, ret, ReFUNCs['FO']['MAXIMUM'](ret))
    ret = FUNCs['FO']['MAXIMUM'][0](ordered_vector)
    print '%s, %d, %s' % (ordered_vector, ret, ReFUNCs['FO']['MAXIMUM'](ret, gcd=3, ordered=True))

def reverse_test():
    ret = FUNCs['FO']['REVERSE'][0](vector)
    print '%s, %s, %s' % (vector, ret, ReFUNCs['FO']['REVERSE'](ret))
    ret = FUNCs['FO']['REVERSE'][0](ordered_vector)
    print '%s, %s, %s' % (ordered_vector, ret, ReFUNCs['FO']['REVERSE'](ret))

def sort_test():
    ret = FUNCs['FO']['SORT'][0](vector)
    print '%s, %s' % (vector, ret)
    print '%s' % ReFUNCs['FO']['SORT'](ret)

def sum_test():
    for x in [-10, -3, 0, 5, 11]:
        print '%d, %s' % (x, ReFUNCs['FO']['SUM'](x))
    for x in [-3, 3, 9]:
        print '%d, %s' % (x, \
                ReFUNCs['FO']['SUM'](x, gcd=3, ordered=True))

def lambadd_test():
    for i in [-10, -2, 0, 9]:
        print "%d=+%s" % (i, ReLambdas['(+)'](i))
    for i in [-9, 9]:
        print "%d=+%s" % (i, ReLambdas['(+)'](i, gcd=3))

def lambdel_test():
    for i in [-10, -2, 0, 9]:
        print "%d=-%s" % (i, ReLambdas['(-)'](i))
    for i in [-9, 9]:
        print "%d=-%s" % (i, ReLambdas['(-)'](i, gcd=3))

def lambmul_test():
    for i in [-10, -2, 0, 9]:
        print "%d=*%s" % (i, ReLambdas['(*)'](i))
    for i in [-9, 9]:
        print "%d=*%s" % (i, ReLambdas['(*)'](i, gcd=3))

def lambmin_test():
    for i in [-10, -2, 0, 9]:
        print "%d, %s" % (i, ReLambdas['MIN'](i))
    for i in [-1, 0, 2]:
        print "%d, %s" % (i, ReLambdas['MIN'](i, gcd=2))

def lambmax_test():
    for i in [-10, -2, 0, 9]:
        print "%d, %s" % (i, ReLambdas['MAX'](i))
    for i in [-1, 0, 2]:
        print "%d, %s" % (i, ReLambdas['MAX'](i, gcd=2))

def filter_p_test():
    v = range(2, 10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(>0)'](v))
    v = range(2, 10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(>0)'](v, gcd=2, ordered=True))

def filter_n_test():
    v = range(-20, -10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(<0)'](v))
    v = range(-20, -10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(<0)'](v, gcd=2, ordered=True))

def filter_e_test():
    v = range(2, 10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(%2==0)'](v))
    v = range(2, 10, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(%2==0)'](v, ordered=True))

def filter_o_test():
    v = range(1, 11, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(%2==1)'](v))
    v = range(1, 11, 2)
    print "%s, %s" % (v, ReFUNCs['HO']['FILTER_(%2==1)'](v, gcd=2, ordered=True))

def map_test():
    v = range(10)
    print "%s%s, %s" % (ReFUNCs['HO']['MAP']('(-1)', v), '(-1)', v)
    print "%s%s, %s" % (ReFUNCs['HO']['MAP']('(+1)', v), '(+1)', v)
    print "%s%s, %s" % (ReFUNCs['HO']['MAP']('(/2)', v), '(/2)', v)
    print "%s%s, %s" % (ReFUNCs['HO']['MAP']('(*(-1))', v), '(*(-1))', v)
    v = [1, 4, 9, 16]
    print "%s%s, %s" % (ReFUNCs['HO']['MAP']('(**2)', v), '(**2)', v)

def count_test():
    n = 5
    print "%d, %s, %s" % (n, '(>0)', ReFUNCs['HO']['COUNT']('(>0)', n))
    print "%d, %s, %s" % (n, '(<0)', ReFUNCs['HO']['COUNT']('(<0)', n))
    print "%d, %s, %s" % (n, '(%2==0)', ReFUNCs['HO']['COUNT']('(%2==0)', n))
    print "%d, %s, %s" % (n, '(%2==1)', ReFUNCs['HO']['COUNT']('(%2==1)', n, gcd=3, ordered=True))

def zipwith_test():
    res = range(10, 20)
    ret = ReFUNCs['HO']['ZIPWITH']('(+)', res)
    print "%s%s%s=%s" % (ret[0], '(+)', ret[1], res)
    ret = ReFUNCs['HO']['ZIPWITH']('(-)', res, gcd = 2)
    print "%s%s%s=%s" % (ret[0], '(-)', ret[1], res)
    ret = ReFUNCs['HO']['ZIPWITH']('(*)', res)
    print "%s%s%s=%s" % (ret[0], '(*)', ret[1], res)
    ret = ReFUNCs['HO']['ZIPWITH']('MIN', res)
    print "%s%s%s=%s" % (ret[0], 'MIN', ret[1], res)
    ret = ReFUNCs['HO']['ZIPWITH']('MAX', res)
    print "%s%s%s=%s" % (ret[0], 'MAX', ret[1], res)

def scanl1_test():
    v = range(10, 20)
    random.shuffle(v)
    print v
    ret = FUNCs['HO']['SCANL1'][0](Lambdas['MAX'][0], v)
    print ret
    ret = ReFUNCs['HO']['SCANL1']('MAX', ret)
    print ret
    print FUNCs['HO']['SCANL1'][0](Lambdas['MAX'][0], ret)

TEST_FUNCs = {
    'head': head_test,
    'last': last_test,
    'take': take_test,
    'drop': drop_test,
    'access': access_test,
    'minimum': minimum_test,
    'maximum': maximum_test,
    'reverse': reverse_test,
    'sort': sort_test,
    'sum': sum_test,
    'lambadd': lambadd_test,
    'lambdel': lambdel_test,
    'lambmul': lambmul_test,
    'lambmin': lambmin_test,
    'lambmax': lambmax_test,
    'filter_p': filter_p_test,
    'filter_n': filter_n_test,
    'filter_e': filter_e_test,
    'filter_o': filter_o_test,
    'map': map_test,
    'count': count_test,
    'zipwith': zipwith_test,
    'scanl1': scanl1_test,
}

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Usage:\n" + \
                "dsl_test.py $FUNC\n" + \
                "param $FUNC: the name of function"
        sys.exit(1)

    TEST_FUNCs[sys.argv[1]]()

