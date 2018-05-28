#!/usr/bin/env python
from functools import partial
from inspect import getsource

import functools

fst      = lambda (a,_): a
snd      = lambda (_,b): b
foldl    = lambda fnc, acc, xs: reduce(fnc, xs, acc)
foldr    = lambda fnc, acc, xs: reduce(fnc, xs[::-1], acc)
co       = lambda *fns: lambda *a, **kw: foldl(lambda _, fnc: fnc(*a, **kw), None, fns)
co       = lambda *fns: lambda *a, **kw: [fnc(*a, **kw) for fnc in fns]
cm       = lambda *fns: lambda *a, **kw: foldr(lambda r, fnc: fnc(*fst(r),**snd(r)) if type(r) is tuple else fnc(r), (a,kw), list(fns))
cur      = functools.partial
filt     = lambda pred, iterable: [i for i in iterable if perd(i)]
Not      = lambda x: not x
Eq       = lambda l, r: l == r
Is       = lambda l, r: l is r
Neq      = cm(Not,Eq)
attr     = lambda name: lambda x: x.getattr(name)
if_else  = lambda pred, true, false: lambda *a, **kw: true(*a, **kw) if pred(*a, **kw) else false(*a, **kw)

class Composable(object):
    def __init__(self, func):
        self._func = func

    # self >> fnc
    def __rshift__(self, func):
        if type(func) is tuple:
            res = Composable(cm(co(*func), self._func))
        else:
            res = Composable(cm(func, self._func))
        return res

    # self << fnc
    def __lshift__(self, func):
        if type(func) is tuple:
            res = Composable(cm(self._func, co(*func)))
        else:
            res = Composable(cm(self._func, func))
        return res

    # fnc >> self
    __rrshift__ = __lshift__

    # fnc << self
    __rlshift__ = __rshift__

    # self * func
    def __mul__(self, func):
        return Composable(lambda *a, **kw: self._func(*func(*a, **kw)))

    # self ** func
    def __pow__(self, func):
        return Composable(lambda *a, **kw: self._func(**func(*a, **kw)))

    # func * self
    def __rmul__(self, func):
        return Composable(lambda *a, **kw: fnc(*self._func(*a, **kw)))

    # func ** self
    def __rpow__(self, func):
        return Composable(lambda *a, **kw: fnc(**self._func(*a, **kw)))

    def __call__(self, *a, **kw):
        return self._func(*a, **kw)

last     = Composable(lambda iterable: iterable[-1])
Id       = Composable(lambda x: x)
call     = lambda *a, **kw: Composable(lambda fnc: fnc(*a, **kw))
const    = lambda x:   Composable(lambda y: x)
#########################################################################################################
#(m a -> b) - > a - > b
#monada_s = lambda func, a: func(a) #(a - > b) -> a - > b
#monada_t = lambda func, a: func(*a) #(*a -> b) -> tupel(a)->b
#monada_d = lambda func, a: func(**a) #(**a -> b) -> dict(a)->b
#
#class ComposableError(Exception):
#    pass
#
#def wrap_arguments(*arg, **kw):
#    def wrapper(*arg_):
#        tmp = iter(arg_)
#        return tuple(next(tmp, a) if a is Id else a for a in iter(arg))
#    return wrapper
#
#class Composable(object):
#    def __init__(self, func, monada):
#        self._func_list = [(func, monada)]
#        self._monada = monada
#
#    @classmethod
#    def make_composable(cls, val, bind_type=monada_s):
#        if type(val) is cls:
#            return val
#        if type(val) is tuple:
#            return cls(wrap_arguments(*val), monada_t)
#        if type(val) is dict:
#            return cls(wrap_arguments(**val), monada_d)
#        if callable(val):
#            return cls(val, bind_type)
#        else:
#            return cls(lambda *a: val, bind_type)
#
#    @classmethod
#    def _bind_composable(cls, comp_1, comp_2):
#        self = cls.__new__(cls)
#        func, _ = comp_2._func_list[0]
#        monada = comp_1._monada
#        self._func_list = comp_1._func_list + [(func, monada)] + comp_2._func_list[1:]
#        self._monada = comp_2._monada
#        return self
#
#    # self >> fnc
#    def __rshift__(self, other_fn):
#        other_fn = self.make_composable(other_fn)
#        return self._bind_composable(self, other_fn)
#
#    # self << fnc
#    def __lshift__(self, other_fn):
#        other_fn = self.make_composable(other_fn)
#        return other_fn >> self
#
#    # fnc >> self
#    __rrshift__ = __lshift__
#
#    # fnc << self
#    __rlshift__ = __rshift__
#
#    def __getattr__(self, name):
#        return self >> (lambda obj: getattr(obj, name))
#
#    def __getitem__(self, name):
#        return self >> (lambda obj: obj[name])
#
#    def __call__(self, *a):
#        func, _ = self._func_list[0]
#        res = func(*a)
#        return reduce(lambda res, (func, monada): monada(func, res), self._func_list[1:], res)
#
#
#def Arguments(*arg, **kw):
#    return Composable.make_composable(arg)
#
#def log(*a):
#    print("@@@ {}".format(a))
#    return a
#
#Id = Composable.make_composable(lambda a: a)
#call = lambda *a: Composable.make_composable(lambda func: func(*a))
#composable = Composable.make_composable
#Log  = Composable.make_composable(log, monada_t)
#fmap = Composable.make_composable(map)
#Args = Arguments
#
#def main():
#    assert(3 == Id(3))
#    assert('test' == (Id << 'test')())
#    assert(33 == ((Id << (lambda: {'d': 33}))['d'])())
#    assert((1,3) == Args(Id, 3)(1))
#    assert((1,3,4) == Args(Id, 3, Id)(1,4))
#    assert((1,3,4) == (Args(Id, 3, Id) << (1, 4))())
#
#if __name__ == '__main__':
#    main()
#
'''
add_one = composable(lambda x: x+1)
add_two = add_one << add_one
get_cutom_str = composable('You typed {}'.format)

res = add_two(10)
a = Args(add_two, Id) >> map << range
a = get_cutom_str << range
print(a(3))

'''
