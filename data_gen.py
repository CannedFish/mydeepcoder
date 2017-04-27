# -*- coding: utf-8 -*-

import sys, pickle

from dsl import FUNCs, Lambdas
from program import Program, Step

PROGRAMs = []

def save(f_path):
    """
    Save data to a file
    """
    global DEBUG
    with open(f_path, 'w+') as f:
        if DEBUG:
            f.writelines(map(lambda x: str(x)[1:-1]+'\n', PROGRAMs))
        else:
            f.writelines(pickle.dumps(PROGRAMs))
    print "Generated programs has been saved at %s" % f_path

def search_next(cur, program, fo_remain, ho_remain, target_len):
    if len(program) == target_len:
        p = Program()
        for s in program:
            p.append_step(Step(*s))
        PROGRAMs.append(p)
        # print p
        return
    else:
        valid_fo_funcs = filter(lambda x: FUNCs['FO'][x][1][0] == cur[2] \
                if len(FUNCs['FO'][x][1]) == 1 \
                else FUNCs['FO'][x][1][1] == cur[2], fo_remain)
        # len(FUNCs['HO'][x][1]) == 2 \ and 
        valid_ho_funcs = filter(lambda x: FUNCs['HO'][x][1][1] == cur[2], ho_remain)
        for func in valid_fo_funcs:
            search_next(FUNCs['FO'][func], \
                    program+[(func,)], \
                    filter(lambda x: x!=func, valid_fo_funcs), \
                    valid_ho_funcs, \
                    target_len)
        for func in valid_ho_funcs:
            for lambs in filter(lambda x: (Lambdas[x][3], Lambdas[x][2])\
                    ==FUNCs['HO'][func][1][0], \
                    [l for l in Lambdas]):
                search_next(FUNCs['HO'][func], \
                        program+[(func, lambs)], \
                        valid_fo_funcs, \
                        filter(lambda x: x!=func, valid_ho_funcs), \
                        target_len)

def main(length, f_path):
    print "Generating programs whose length is %d..." % length
    fo_funcs = [func for func in FUNCs['FO']]
    ho_funcs = [func for func in FUNCs['HO']]
    for func in fo_funcs:
        search_next(FUNCs['FO'][func], \
                [(func,)], \
                filter(lambda x: x!=func, fo_funcs), \
                ho_funcs, \
                length)
    for func in ho_funcs:
        for lambs in filter(lambda x: (Lambdas[x][3], Lambdas[x][2])\
                ==FUNCs['HO'][func][1][0], \
                [l for l in Lambdas]):
            search_next(FUNCs['HO'][func], \
                    [(func, lambs)], \
                    fo_funcs, \
                    filter(lambda x: x!=func, ho_funcs), \
                    length)
    save(f_path)
    print "Prepare input-output for programs..."
    no = 0
    for program in PROGRAMs:
        print 'No %d' % no
        no += 1
        # TODO: generate through forword direction
        print 'Samples: %s\n' % program.generate_func_in()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python data_gen.py $Length[ $File $DEBUG]\n" +\
                "Param $Length: the length of programe\n" +\
                "Param $File: the path of file to save\n" +\
                "Param $DEBUG: True or False\n"
        sys.exit(1)

    f_path = './generated_data.dat' \
            if len(sys.argv)<3 or sys.argv[2]=='-' \
            else sys.argv[2]
    global DEBUG
    DEBUG = True \
            if len(sys.argv)<4 or sys.argv[3]=='-' else \
            sys.argv[3]=='True'
    main(int(sys.argv[1]), f_path)

