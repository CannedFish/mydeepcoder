# -*- coding: utf-8 -*-

from dsl import FUNCs, Lambdas, ReFUNCs, ReLambdas, \
        initial_list, initial_int, key_of_attr, TYPE

class Step(object):
    def __init__(self, step_func, step_lambda=None):
        self._gcd = 1
        self._ordered = False
        self._func = step_func
        self._lambda = step_lambda
        self._multi_param = False
        self._reversed = False
        self._oddeven = None
        self._sign = None
        # TODO: sqrt 2?

        if step_lambda == None:
            self._func_type = 'FO'
            self._step_func = FUNCs['FO'][step_func]
            self._step_refunc = ReFUNCs['FO'][step_func]
            if step_func == 'SORT':
                self._ordered = True
            elif step_func == 'REVERSE':
                self._reversed = True
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
            elif step_lambda == '(%2==0)':
                self._oddeven = 0
            elif step_lambda == '(%2==1)':
                self._oddeven = 1
            elif step_lambda == '(>0)':
                self._sign = 1
            elif step_lambda == '(<0)':
                self._sign = -1
            if len(self._step_func[1]) > 2:
                self._multi_param = True

    def __str__(self):
        return "(%s, %s)" % (self._func, self._lambda)

    @property
    def funcs(self):
        ret = [self._func]
        if self._lambda is not None:
            ret.append(self._lambda)
        return ret

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

    def step_in(self, step_out, **kwargs):
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
        return self._step_refunc(step_out, **kwargs)

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

    def step_reveresd(self, reversed_now):
        """
        Return ordered after this step, use xor
        """
        return reversed_now ^ self._reversed

    def step_oddeven(self, oddeven_now):
        # TODO: How to consider previous status
        return self._oddeven

    def step_sign(self, sign_now):
        """
        -1 means negative
        1 means positive
        0 means zero
        """
        if self._sign is None:
            return sign_now
        if sign_now is None:
            return self._sign
        if sign_now != self._sign:
            return 0
        return sign_now

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
        # [Step, Step, ...]
        self._steps = []
        # [[{'-2': param1, '-1': param2}, result], ...]
        self._samples = []
        # {'key2': [['key0', 'key1'], 'key2']}
        self._exec_flow = {}
        # {'key': 0 or 1}
        self._attr = {}
        self._attr.fromkeys(key_of_attr(), 0)
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
        for func in step.funcs:
            self._attr[func] = 1
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

    def _dfs_exec(self, step_now, func_out, **kw): # gcd, ordered, _reversed, oddeven
        if step_now == len(self._steps)-1:
            if func_out == None:
                if self._steps[-1].step_output_type == 0:
                    func_out = initial_int(self._steps[-1].step_gcd(kw['gcd']))
                    init_p = func_out
                elif self._steps[-1].step_output_type == 1:
                    func_out = initial_list(gcd=self._steps[-1].step_gcd(kw['gcd']), \
                            ordered=self._steps[-1].step_ordered(kw['ordered']), \
                            _reversed=self._steps[-1].step_reveresd(kw['_reversed']), \
                            oddeven=self._steps[-1].step_oddeven(kw['oddeven']), \
                            sign=self._steps[-1].step_oddeven(kw['sign']))
                    # deep copy
                    init_p = []
                    init_p.extend(func_out)
            return self._steps[step_now].step_in(init_p, gcd=kw['gcd'], \
                    ordered=kw['ordered'], _reversed=kw['_reversed']), [{}, func_out]
        _step_in, _out = self._dfs_exec(step_now+1, func_out, \
                gcd=self._steps[step_now].step_gcd(kw['gcd']), \
                ordered=self._steps[step_now].step_ordered(kw['ordered']), \
                _reversed=self._steps[step_now].step_reveresd(kw['_reversed']), \
                oddeven=self._steps[step_now].step_oddeven(kw['oddeven']), \
                sign=self._steps[step_now].step_oddeven(kw['sign']))
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
        # print 'Step: %d, Step in: %s, Out: %s' % (step_now+1, _step_in, _out)
        return self._steps[step_now].step_in(_step_out, gcd=kw['gcd'], \
                ordered=kw['ordered'], _reversed=kw['_reversed']), _out

    def generate_func_in(self, func_out=None):
        """
        Return a valid input of this program based on the output.
        """
        # generate
        kw = {
            'gcd': 1,
            'ordered': False,
            '_reversed': False,
            'oddeven': None,
            'sign': None
        }
        for i in range(5):
            _step_in, _out = self._dfs_exec(0, func_out, **kw)
            if type(_step_in)==tuple:
                params = _step_in
            else:
                params = (_step_in, )
            for param, i in zip(params, range(len(params))):
                _out[0][self._exec_flow['0'][0][i]] = param
            # print 'Step: %d, Step in: %s, Out: %s' % (0, _step_in, _out)
            self._samples.append(_out)
        # verify
        a, b = self.verify(self._samples)
        if a != b:
            print str(self)
            import pdb
            pdb.set_trace()

        return self._samples

    def execute(self, func_in):
        """
        Execute this program and return the result.
        """
        # check the number of parameters
        if len(func_in) != self._param_num:
            print "Parameter number Error"
            return 

        # check the type of parameters
        params_type = sorted([s for s in self._exec_flow.items() \
                if int(s[0]) < 0], key=lambda x: int(x[0]))
        for param, p_target in zip(func_in, params_type):
            if type(param) == int:
                p_type = 0
            elif type(param) == list and type(param[0]) == int:
                p_type = 1
            else:
                p_type = -1
            if p_type != p_target[1][2]:
                print "Parameter type Error, should be %s" % \
                        tuple([TYPE[p[1][2]] for p in params_type])
                return 

        # execute
        # travel exec_flow from minimun idx
        progress = [p for p in func_in] # cache input of each step
        progress.extend([None]*len(self._steps))
        exec_order = sorted(self._exec_flow.keys(), key=lambda x: int(x))
        result = []
        for s, i in zip(exec_order, range(len(exec_order))):
            next_s = self._exec_flow[s][1]
            if next_s is not None:
                next_p = int(next_s) + self._param_num
                if progress[next_p] is None:
                    progress[next_p] = [0]*len(self._exec_flow[next_s][0])
                idx = self._exec_flow[next_s][0].index(s)
                if int(s) < 0:
                    progress[next_p][idx] = progress[i]
                else:
                    step = self._steps[int(s)]
                    ret = step.step_out(*tuple(progress[int(s)+self._param_num]))
                    progress[next_p][idx] = ret
            else:
                step = self._steps[int(s)]
                result = step.step_out(*tuple(progress[int(s)+self._param_num]))
        
        return result

    def verify(self, samples):
        """
        :param samples: [({'-2': param1, '-1': param2, ...}, result), ...]
        """
        ok = 0
        for sample in samples:
            ss = sorted([p for p in sample[0].items()], \
                    key=lambda x: int(x[0]))
            ret = self.execute(tuple([s[1] for s in ss]))
            if ret == sample[1]:
                print "%s OK" % sample
                ok += 1
            else:
                print "Failed: %s, sample is %s, result is %s" % \
                        (sample[0], sample[1], ret)
        print "%d samples tested, ok persent is %d/%d" \
                % (len(samples), ok, len(samples))
        return ok, len(samples)

    def export(self):
        """
        :return: (p, a, e)
        p --> Program (steps)
        a --> Attributes (attr)
        e --> Examples (samples) [5, 4] (input_type, input, output_type, output)
        """
        samples = []
        for s in self._samples:
            if len(s[0].keys()) > 1:
                # TODO: handle two more parameters


