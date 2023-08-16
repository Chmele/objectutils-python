from functools import singledispatch
from types import FunctionType
from types import BuiltinFunctionType


def get_all_keys(iter):
    try:
        return iter.keys()
    except AttributeError:
        return range(len(iter))


class PathGroup:
    def __init__(self, *paths, type=list):
        self.paths = paths
        self.type = type

    def traverse_iter(self, o, rest):
        yield from (deep_traverse(o, (*path, *rest)) for path in self.paths)

    def traverse(self, o, rest):
        return self.type(self.traverse_iter(o, rest))


def deep_traverse(o, path):
    try:
        p, *rest = path
    except ValueError:
        return o
    return traverse_item(p, o)(rest)
        

@singledispatch
def traverse_item(p, o):
    return lambda rest: deep_traverse(o[p], rest)

@traverse_item.register
def _(p: list, o):
    return lambda rest: type(p)([deep_traverse(o, (key, *rest)) for key in p or get_all_keys(o)])

@traverse_item.register
def _(p: PathGroup, o):
    return lambda rest: p.traverse(o, rest)

# @traverse_item.register(type(lambda x: x))
@traverse_item.register(BuiltinFunctionType)
@traverse_item.register(FunctionType)
def _(p: type(deep_traverse), o):
    return lambda rest: p(deep_traverse(o, rest))