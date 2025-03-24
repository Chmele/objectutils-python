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
        return type(p)(deep_traverse(o, (index, *rest)) for index in p or get_all_keys(o))
    except ValueError:
        return o
    except TypeError:
        return deep_traverse(o[p], rest)
