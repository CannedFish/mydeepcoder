# -*- coding: utf-8 -*-

from dsl import FUNCs, Lambdas, ReFUNCs, ReLambdas, \
        initial_list, initial_int

class Step(object):
    def __init__(self, step_func, step_lambda=None):
        self._gcd = 1
        self._ordered = False
        self._func = step_func
        self._lambda = step_lambda
        self._multi_param = False
        if step_lambda == None:
            self._func_type = 'FO'
            self._step_func = FUNCs['FO'][step_func]
            self._step_refunc = ReFUNCs['FO'][step_func]
            if step_func == 'SORT':
                self._ordered = True
            if len(self._step_func[1]) > 1:
                self._multi_param = True
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
            if len(self._step_func[1]) > 2:
                self._multi_param = True
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

    def step_in(self, step_out):
        """
        Return a step_in based on a step_out
        """
        if self._func_type == 'FO' and \
                not self._type_check(step_out, \
                    self._step_func[2]) or \
                self._func_type == 'HO' and \
                not self._type_check(step_out, \
                    self._step_func[2]):
            print '%s step out type error' % self._step_func
            return None
        if self._func_type == 'HO':
            return self._step_refunc(self._lambda, step_out)
        return self._step_refunc(step_out)

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
    def multi_param(self):
        return self._multi_param

    @property
    def param_type(self):
        return self._step_func[1]

    @property
    def step_output_type(self):
        return self._step_func[2]

class Program(object):
    def __init__(self):
        self._steps = []
        self._samples = []
        # {'key2': [['key0', 'key1'], 'key2']}
        self._exec_flow = {}
        self._param_num = 0

    def __str__(self):
        return str([str(step) for step in self._steps])

    def _add_param(self, idx, p_type):
        """
        param idx: the index of step use this parameter
        return: the index of this parameter
        """
        self._param_num += 1
        self._exec_flow[str(-self._param_num)] = [None, idx, p_type]
        return str(-self._param_num)

    def _add_step(self, idx, prev_idx, p_num=1, p_idx=0):
        """
        param idx: the index of step use this parameter
        param prev_idx: the index of step before this step
        param p_num: the number of p_num
        param p_idx: the index of this parameter
        """
        if not self._exec_flow.has_key(idx):
            self._exec_flow[idx] = [[0]*p_num, None]
        self._exec_flow[idx][0][p_idx] = prev_idx
        self._exec_flow[prev_idx][1] = idx

    def append_step(self, step):
        if type(step) != Step:
            raise TypeError('Should be an instance of Step, not %s', type(step))
        self._steps.append(step)
        # Update the execution flow
        prev_res = None
        step_idx = len(self._steps)-1
        for f in self._exec_flow.items():
            if f[1][1] is None:
                prev_res = f[0]
                break
        if prev_res is None:
            if step.multi_param:
                param_num = 2
            else:
                param_num = 1
            for i, p_type in zip(range(param_num), step.param_type):
                p_idx = self._add_param(str(step_idx), p_type)
                self._add_step(str(step_idx), p_idx, param_num, i)
        else:
            if step.multi_param:
                prev_step = self._steps[int(prev_res)]
                pr_type = prev_step.step_output_type
                param_num = len(step.param_type)
                for pa, i in zip(step.param_type, range(param_num)):
                    if pr_type == pa:
                        self._add_step(str(step_idx), prev_res, param_num, i)
                    else:
                        self._add_step(str(step_idx), \
                                self._add_param(str(step_idx), pa), param_num, i)
            else:
                self._add_step(str(step_idx), prev_res)

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
            return self._steps[step_now].step_in(init_p), [{}, func_out]
        _step_in, _out = self._dfs_exec(step_now+1, func_out, \
                self._steps[step_now].step_gcd(gcd), \
                self._steps[step_now].step_ordered(ordered))
        flow = self._exec_flow[str(step_now+1)]
        _step_out = None
        if type(_step_in) == tuple:
            for p, i in zip(flow[0], range(len(flow))):
                if int(p) < 0:
                    _out[0][p] = _step_in[i]
                else:
                    _step_out = _step_in[i]
        else:
            _step_out = _step_in
        return self._steps[step_now].step_in(_step_out), _out

    def generate_func_in(self, func_out=None):
        """
        Return a valid input of this program based on the output.
        """
        import pdb
        pdb.set_trace()
        for i in range(5):
            in_out = self._dfs_exec(0, func_out, 1, False)
            in_out[1][0][self._exec_flow['0'][0][0]] = in_out[0]
            self._samples.append(in_out[1])
        return self._samples

    def execute(self, func_in):
        """
        Execute this program and return the result.
        """
        # TODO: travel exec_flow from minimun idx
        return []

