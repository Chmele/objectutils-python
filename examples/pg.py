from examples.samples import a, b
from src.main import *
from src.traverse import deep_traverse

def make_filter(predicate):
    return lambda iter: [i for i in iter if predicate(i)]

a = deep_traverse(b, ("e", make_filter(lambda x: x>2), [], "x"))
print(a)
