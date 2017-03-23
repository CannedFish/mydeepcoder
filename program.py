# -*- coding: utf-8 -*-

from dsl import FUNCs, Lambdas, ReFUNCs, ReLambdas

class Step(object):
    def __init__(self, step_func, step_lambda=None):
        if step_lambda == None:
            self._func_type = 'FO'
            self._step_func = FUNCs['FO'][step_func]
        else:
            self._func_type = 'HO'
            self._step_func = FUNCs['HO'][step_func]
            self._step_lambda = Lambdas[step_lambda]

    def _type_check(self, var, tar_type):
        src_type = -1
        if type(var) == int:
            src_type = 0
        elif type(var) == list:
            if type(var[0]) = int:
                src_type = 1
        else:
            return False

        return True if src_type == tar_type else False

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

    def step_in(self, step_out):
        """
        Return a step_in based on a step_out
        """
        if self._func_type == 'FO' and \
                not self._type_check(step_in, \
                    self._step_func[2]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_in, \
                    self._step_func[2]):
            print '%s step out type error' % self._step_func
            return None
        return self._reverse_exec()

    def step_gcd(self, gcd_now):
        """
        Return gcd after this step
        """
        return gcd_now*1

    def step_ordered(self, ordered_now):
        """
        Return ordered after this step
        """
        return ordered_now or False

class Program(object):
    def __init__(self):
        self._steps = []
        # NOTE: Let Step do it self
        # self._gcd = 1

    # def _check_divisible(self, step):
        # """
        # Check if this program has operations like *2, *3, etc,
        # and make sure results after /2, /3, etc are integers.
        # Modify the greatest common divisor.
        # """
        # self._gcd = 1

    def append_step(step):
        # TODO: check divisible
        self._steps.append(step)

    def _dfs_exec(self, step_now, func_out, gcd, ordered):
        if step_now == len(self._steps)-1:
            return self._steps[step_now].step_in(func_out)
        _step_in = _dfs_exec(step_now+1, func_out, \
                self._steps[step_now].step_gcd(gcd), \
                self._steps[step_now].step_ordered(ordered))
        return self._steps[step_now].step_in(_step_in)

    def generate_func_in(self, func_out):
        """
        Return a valid input of this program based on the output.
        """
        # TODO: Maybe I can use a recurrent method
        return self._dfs_exec(0, func_out, 1, False)

    def exec(self, func_in):
        """
        Execute this program and return the result.
        """
        # TODO: travel steps
        return []

