# -*- coding: utf-8 -*-

from dsl import FUNCs, Lambdas

class Step(object):
    def __init__(self, step_func, step_lambda=None):
        if step_lambda == None:
            self._func_type = 'FO'
            self._step_func = FUNCs['FO'][step_func]
        else:
            self._func_type = 'HO'
            self._step_func = FUNCs['HO'][step_func]
            self._step_lambda = Lambdas[step_lambda]

    def _type_check(var, tar_type):
        src_type = -1
        if type(var) == int:
            src_type = 0
        elif type(var) == list:
            if type(var[0]) = int:
                src_type = 1
        else:
            return False

        return True if src_type == tar_type else False

    @property
    def step_out(self, step_in):
        """
        Return a step_out based on a step_in
        """
        if self._func_type == 'FO' and \
                not self._type_check(step_in, \
                    self._step_func[1][0]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_in, \
                    self._step_func[1][1]):
            print '%s step in type error' % self._step_func
            return None
        return self._step_func[0](step_in)

    def _reverse_exec(self, step_out):
        return None

    @property
    def step_in(self, step_out):
        if self._func_type == 'FO' and \
                not self._type_check(step_in, \
                    self._step_func[2]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_in, \
                    self._step_func[2]):
            print '%s step out type error' % self._step_func
            return None
        return self._reverse_exec()

class Program(object):
    def __init__(self):
        self._steps = []
        self._gcd = 1

    def _check_divisible(self, step):
        """
        Check if this program has operations like *2, *3, etc,
        and make sure results after /2, /3, etc are integers.
        Modify the greatest common divisor.
        """
        self._gcd = 1

    def append_step(step):
        # TODO: check divisible
        self._steps.append(step)

    def generate_func_in(self, func_out):
        """
        Return a valid input of this program based on the output.
        """
        # TODO: Maybe I can use a recurrent method
        return []

    def exec(self, func_in):
        """
        Execute this program and return the result.
        """
        # TODO: travel steps
        return []

