#!/usr/bin/env python
from functools import partial
from inspect import getsource

#(m a -> b) - > a - > b
monada_s = lambda func, a: func(a) #(a - > b) -> a - > b
monada_t = lambda func, a: func(*a) #(*a -> b) -> tupel(a)->b
monada_d = lambda func, a: func(**a) #(**a -> b) -> dict(a)->b


class ComposableError(Exception):
    pass

def wrap_arguments(*arg, **kw):
    def wrapper(*arg_):
        tmp = iter(arg_)
        return tuple(next(tmp, a) if a is Id else a for a in iter(arg))
    return wrapper

class Composable(object):
    def __init__(self, func, monada):
        self._func_list = [(func, monada)]
        self._monada = monada

    @classmethod
    def make_composable(cls, val, bind_type=monada_s):
        if type(val) is cls:
            return val
        if type(val) is tuple:
            return cls(wrap_arguments(*val), monada_t)
        if type(val) is dict:
            return cls(wrap_arguments(**val), monada_d)
        if callable(val):
            return cls(val, bind_type)
        else:
            return cls(lambda *a: val, bind_type)

    @classmethod
    def _bind_composable(cls, comp_1, comp_2):
        self = cls.__new__(cls)
        func, _ = comp_2._func_list[0]
        monada = comp_1._monada
        self._func_list = comp_1._func_list + [(func, monada)] + comp_2._func_list[1:]
        self._monada = comp_2._monada
        return self

    # self >> fnc
    def __rshift__(self, other_fn):
        other_fn = self.make_composable(other_fn)
        return self._bind_composable(self, other_fn)

    # self << fnc
    def __lshift__(self, other_fn):
        other_fn = self.make_composable(other_fn)
        return other_fn >> self

    # fnc >> self
    __rrshift__ = __lshift__

    # fnc << self
    __rlshift__ = __rshift__

    def __getattr__(self, name):
        return self >> (lambda obj: getattr(obj, name))

    def __getitem__(self, name):
        return self >> (lambda obj: obj[name])

    def __call__(self, *a):
        func, _ = self._func_list[0]
        res = func(*a)
        return reduce(lambda res, (func, monada): monada(func, res), self._func_list[1:], res)


def Arguments(*arg, **kw):
    return Composable.make_composable(arg)

def log(*a):
    print("@@@ {}".format(a))
    return a

Id = Composable.make_composable(lambda a: a)
call = lambda *a: Composable.make_composable(lambda func: func(*a))
composable = Composable.make_composable
Log  = Composable.make_composable(log, monada_t)
fmap = Composable.make_composable(map)
Args = Arguments

def main():
    assert(3 == Id(3))
    assert('test' == (Id << 'test')())
    assert(33 == ((Id << (lambda: {'d': 33}))['d'])())
    assert((1,3) == Args(Id, 3)(1))
    assert((1,3,4) == Args(Id, 3, Id)(1,4))
    assert((1,3,4) == (Args(Id, 3, Id) << (1, 4))())

if __name__ == '__main__':
    main()

'''
add_one = composable(lambda x: x+1)
add_two = add_one << add_one
get_cutom_str = composable('You typed {}'.format)

res = add_two(10)
a = Args(add_two, Id) >> map << range
a = get_cutom_str << range
print(a(3))

'''
