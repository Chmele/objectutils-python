class O:
    def __init__(self, o):
        self.o = o

    def __getitem__(self, item):
        return self.o[item]

    def get_all_keys(self):
        try:
            return self.o.keys()
        except AttributeError:
            return range(len(self.o))
    def __str__(self):
        return str(self.o)


class pathitem:
    def __init__(self, token):
        self.token = token

    def __call__(self, o, func):
        return self.traverse(o, func)
    
    def traverse(self, o, func, *args):
        pass


class indexkey(pathitem):
    def traverse(self, o, func=None):
        return o[self.token]


class listitem(pathitem):
    def traverse(self, o, func, *args):
        return type(self.token)(func(o, (index, *args)) for index in self.token or o.get_all_keys)
    
import functools

def deep_traverse(o, path):
    o = O(o)
    path = [listitem(p) for p in path]
    return functools.reduce(lambda current, p: p.traverse(current), path, o)
