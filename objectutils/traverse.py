from functools import singledispatch
from types import FunctionType, BuiltinFunctionType


def fallback(mapping=None):
    mapping = mapping or {}
    def dec(func):
        def wrapper(*args, exception=None, **kwargs):
            if exception == None:
                return func(*args, **kwargs)
            try:
                return mapping[type(exception)](*args, **kwargs)
            except Exception as e:
                raise exception
        return wrapper 
    return dec


@singledispatch
def get_all_keys(iter):
    pass
    
@get_all_keys.register(tuple)
@get_all_keys.register(list)
def _(key):
    return range(len(key))

@get_all_keys.register
def _(key: dict):
    return key.keys()


class PathGroup:
    def __init__(self, *paths, type=list):
        self.paths = paths
        self.type = type

    def traverse_iter(self, o, rest):
        yield from (traverse(o, (*path, *rest)) for path in self.paths)

    def traverse(self, o, rest):
        return self.type(self.traverse_iter(o, rest))


def traverse(o, path):
    try:
        p, *rest = path
    except ValueError:
        return o
    try:
        return traverse_item(p, o)(rest)
    except Exception as e:
        return traverse_item(p, o, exception=e)(rest)


@singledispatch
@fallback()
def traverse_item(p, o):
    return lambda rest: traverse(o[p], rest)

@traverse_item.register(list)
@fallback()
def process_list(p, o):
    return lambda rest: type(p)([traverse(o, (key, *rest)) for key in p or get_all_keys(o)])

@traverse_item.register(PathGroup)
@fallback()
def process_pathgroup(p, o):
    return lambda rest: p.traverse(o, rest)

def unpacked_args_handler(p, o):
    return lambda rest: p(traverse(o, rest))

@traverse_item.register(type)
@traverse_item.register(BuiltinFunctionType)
@traverse_item.register(FunctionType)
@fallback({
    TypeError: unpacked_args_handler
})
def process_func_item(p, o):
    return lambda rest: p(*traverse(o, rest))

@traverse_item.register(dict)
def process_dict_item(p, o):
    return lambda rest: {key: traverse(o, (*item, *rest)) for key, item in p.items()}
