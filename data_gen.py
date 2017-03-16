# -*- coding: utf-8 -*-

import sys

from dsl import First_Order, High_Order, Lambdas

def save(f_path):
    """
    Save data to a file
    """
    print f_path

def main(length, f_path):
    print length
    save(f_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python data_gen.py $Length[ $File]\n" +\
                "Param $Length: the length of programe\n" +\
                "Param $File: the path of file to save"
        sys.exit(1)

    f_path = './generated_data' if len(sys.argv)<3 else sys.argv[2]
    main(sys.argv[1], f_path)

