#!/usr/bin/env python
from functools import partial
from inspect import getsource

class ComposableError(Exception):
    pass

def wrap_arguments(*arg, **kw):
    def wrapper(*arg_):
        tmp = iter(arg_)
        return tuple(next(tmp, a) if a is Id else a for a in iter(arg))
    return wrapper

class composable(object):
    def __init__(self, func):
        if type(func) is composable:
            self._func = func._funcs
        else:
            self._func = func

    # self >> fnc
    def __rshift__(self, other_fn):
        if type(other_fn) is not composable:
            other_fn = Composable(other_fn)._func
        return composable(self._func + other_fn)

    # self << fnc
    def __lshift__(self, other_fn):
        if type(other_fn) is not composable:
            other_fn = Composable(other_fn)._func
        return composable(other_fn + self._func)

    # fnc >> self
    __rrshift__ = __lshift__

    # fnc << self
    __rlshift__ = __rshift__

    def __getattr__(self, name):
        return composable(self._func + [lambda obj: getattr(obj, name)])

    def __getitem__(self, name):
        return composable(self._func + [lambda obj: obj[name]])

    def __call__(self, *a):
        a = self._func[0](*a)
        return reduce(lambda res, func: func(res), self._func[1:], a)


def Arguments(*arg, **kw):
    return composable([lambda x: wrap_arguments(*arg, **kw)(*x) if type(x) is tuple else wrap_arguments(*arg, **kw)(*x)])


def Composable(func=lambda a: a):
    if type(func) is tuple:
        return Arguments(*func)
    if type(func) is dict:
        return Arguments(**func)
    if type(func) is str:
        return composable([lambda *a: func])
    if type(func) is composable:
        return composable(func._func)
    if callable(func):
        return composable([func])

def log(*a):
    print("@@@ {}".format(a))
    return a

Id = Composable()

#uncurry = composable(rr, tuple)
#curry = Id

Log = Composable([log])
Args = Arguments
fmap = Composable(map)

def main():
    #assert(3 == Id(3))
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
