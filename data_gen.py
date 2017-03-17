# -*- coding: utf-8 -*-

import sys

from dsl import FUNCs, Lambdas

PROGRAM = []

def save(f_path):
    """
    Save data to a file
    """
    with open(f_path, 'w+') as f:
        f.writelines(map(lambda x: str(x)[1:-1]+'\n', PROGRAM))
    print "Generated programs has been saved at %s" % f_path

def search_next(cur, program, fo_remain, ho_remain, target_len):
    if len(program) == target_len:
        PROGRAM.append(program)
        print program
        return
    else:
        # NOTE: tunable
        # How can I put functions like ZIPWITH after 2 functions which 
        # produce an integer array?
        valid_fo_funcs = filter(lambda x: FUNCs['FO'][x][1][0] == cur[2] \
                if len(FUNCs['FO'][x][1]) == 1 \
                else FUNCs['FO'][x][1][1] == cur[2], fo_remain)
        valid_ho_funcs = filter(lambda x: len(FUNCs['HO'][x][1]) == 2 \
                and FUNCs['HO'][x][1][1] == cur[2], ho_remain)
        for func in valid_fo_funcs:
            search_next(FUNCs['FO'][func], \
                    program+[func], \
                    filter(lambda x: x!=func, valid_fo_funcs), \
                    valid_ho_funcs, \
                    target_len)
        for func in valid_ho_funcs:
            search_next(FUNCs['HO'][func], \
                    program+[func], \
                    valid_fo_funcs, \
                    filter(lambda x: x!=func, valid_ho_funcs), \
                    target_len)

def main(length, f_path):
    print "Generating programs whose length is %d" % length
    fo_funcs = [func for func in FUNCs['FO']]
    ho_funcs = [func for func in FUNCs['HO']]
    for func in fo_funcs:
        search_next(FUNCs['FO'][func], \
                [func], \
                filter(lambda x: x!=func, fo_funcs), \
                ho_funcs, \
                length)
    for func in ho_funcs:
        search_next(FUNCs['HO'][func], \
                [func], \
                fo_funcs, \
                filter(lambda x: x!=func, ho_funcs), \
                length)
    save(f_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python data_gen.py $Length[ $File]\n" +\
                "Param $Length: the length of programe\n" +\
                "Param $File: the path of file to save"
        sys.exit(1)

    f_path = './generated_data.dat' if len(sys.argv)<3 else sys.argv[2]
    main(int(sys.argv[1]), f_path)

