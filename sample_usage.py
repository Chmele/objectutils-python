from examples.samples import task as correct, task2 as answer
from src.main import *


class Mistake:
    def __init__(self, minus, text, *args):
        self.minus = minus
        self.text = text
        self.args = args

    def __str__(self):
        return self.text.format(*self.args)



mark_match = {
    (0,): 0.25,
    (1,): 0.25,
    (2,): 0.25,
    (3, "rows", (),"cells", 0, "content"): 0.15,
    (3, "rows", (),"cells", 1, "content"): 0.25,
    (3, 'rows', (), 'cells', (2, 3), 'content'): 0.6,
    (3, "rows", -1, 'cells', (), 'content'): 0.25
}
mark = 0

def exact_path_match_pattern(path, pattern):
    def compare(itempath, itempattern):
        if itempattern == [] or itempattern == ():
            return True
        try:
            return itempath in itempattern
        except TypeError:
            return itempath == itempattern
    
    return [
        itempath for itempath, itempattern 
        in zip(path, pattern) if compare(itempath, itempattern)
    ]

print(exact_path_match_pattern(flatten(per_itempair(answer, correct)), (3, "rows", (),"cells", 0, "content")))
