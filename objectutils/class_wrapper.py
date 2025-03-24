from .single_dispatch import deep_traverse
from collections import UserDict


class T(UserDict):
    def __getitem__(self, key):
        try:
            return deep_traverse(self.data, key)
        except TypeError:
            return super().__getitem__(key)
