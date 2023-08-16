from single_dispatch import deep_traverse
from collections import UserDict


class T(UserDict):
    def __getitem__(self, key):
        return deep_traverse(self.data, key)
