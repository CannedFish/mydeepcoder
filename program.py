# -*- coding: utf-8 -*-

from dsl import FUNCs, Lambdas, ReFUNCs, ReLambdas, \
        initial_list, initial_int

class Step(object):
    def __init__(self, step_func, step_lambda=None):
        self._gcd = 1
        self._ordered = False
        self._func = step_func
        self._lambda = step_lambda
        self._next = None
        self._prev = []
        if step_lambda == None:
            self._func_type = 'FO'
            self._step_func = FUNCs['FO'][step_func]
            self._step_refunc = ReFUNCs['FO'][step_func]
            if step_func == 'SORT':
                self._ordered = True
        else:
            self._func_type = 'HO'
            self._step_func = FUNCs['HO'][step_func]
            self._step_lambda = Lambdas[step_lambda]
            self._step_refunc = ReFUNCs['HO'][step_func]
            if step_lambda == '(*2)':
                self._gcd = 2
            elif step_lambda == '(*3)':
                self._gcd = 3
            elif step_lambda == '(*4)':
                self._gcd = 4
            # TODO: odd or even?
            # TODO: sqrt 2?
            # TODO: positive or negative?

    def __str__(self):
        return "(%s, %s)" % (self._func, self._lambda)

    def _type_check(self, var, tar_type):
        src_type = -1
        if type(var) == int:
            src_type = 0
        elif type(var) == list:
            if type(var[0]) == int:
                src_type = 1
        else:
            return False

        return True if src_type == tar_type else False

    def step_out(self, *step_in):
        """
        Return a step_out based on a step_in
        """
        if self._func_type == 'FO' and \
                not self._type_check(step_in[0], \
                    self._step_func[1][0]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_in[0], \
                    self._step_func[1][1]):
            print '%s step in type error' % self._step_func
            return None
        if self._func_type == 'HO':
            return self._step_func[0](self._step_lambda[0], *step_in)
        return self._step_func[0](*step_in)

    def step_in(self, *step_out):
        """
        Return a step_in based on a step_out
        """
        if self._func_type == 'FO' and \
                not self._type_check(step_out[0], \
                    self._step_func[2]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_out[0], \
                    self._step_func[2]):
            print '%s step out type error' % self._step_func
            return None
        if self._func_type == 'HO':
            return self._step_refunc(self._lambda, *step_out)
        return self._step_refunc(*step_out)

    def step_gcd(self, gcd_now):
        """
        Return gcd after this step
        """
        return gcd_now*self._gcd

    def step_ordered(self, ordered_now):
        """
        Return ordered after this step
        """
        return ordered_now or self._ordered

    @property
    def step_output_type(self):
        return self._step_func[2]

    @property
    def next_step(self):
        return self._next

    @next_step.setter
    def next_step(self, val):
        self._next = val

    @property
    def prev_step(self):
        return self._prev

    @prev_step.setter
    def prev_step(self, val):
        self._prev.append(val)

class Program(object):
    def __init__(self):
        self._steps = []
        self._samples = []
        self._param_stack = []
        # NOTE: Let Step do it self
        # self._gcd = 1

    # def _check_divisible(self, step):
        # """
        # Check if this program has operations like *2, *3, etc,
        # and make sure results after /2, /3, etc are integers.
        # Modify the greatest common divisor.
        # """
        # self._gcd = 1

    def __str__(self):
        return str([str(step) for step in self._steps])

    def append_step(self, step):
        if type(step) != Step:
            raise TypeError('Should be an instance of Step, not %s', type(step))
        self._steps.append(step)

    def _dfs_exec(self, step_now, func_out, gcd, ordered):
        if step_now == len(self._steps)-1:
            if func_out == None:
                if self._steps[-1].step_output_type == 0:
                    func_out = initial_int(self._steps[-1].step_gcd(gcd))
                    init_p = func_out
                elif self._steps[-1].step_output_type == 1:
                    func_out = initial_list(self._steps[-1].step_gcd(gcd), \
                            self._steps[-1].step_ordered(ordered))
                    init_p = []
                    init_p.extend(func_out)
            return self._steps[step_now].step_in(init_p), func_out
        _step_in, _out = self._dfs_exec(step_now+1, func_out, \
                self._steps[step_now].step_gcd(gcd), \
                self._steps[step_now].step_ordered(ordered))
        # TODO: Put parameters into param_stack
        if len(_step_in) > 1:
            for si in _step_in:
                _s = self._steps[step_now].step_in(si)
                if _s != None:
                    return tuple([_s]+[x for x in _step_in if x != si]), _out
        return self._steps[step_now].step_in(*_step_in), _out

    def generate_func_in(self, func_out=None):
        """
        Return a valid input of this program based on the output.
        """
        import pdb
        pdb.set_trace()
        in_out = self._dfs_exec(0, func_out, 1, False)
        self._samples.append(in_out)
        return in_out

    def execute(self, func_in):
        """
        Execute this program and return the result.
        """
        # TODO: travel steps
        return []

