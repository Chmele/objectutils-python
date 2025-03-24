from objectutils import zip_dicts
from unittest import TestCase


class TestListSum(TestCase):
    def test_list_sum_default(self):
        l1 = [1,2,{}]
        l2 = [2,3,{}]
        self.assertEqual(zip_dicts(l1, l2), {0: (1, 2), 1: (2, 3)})


class TestDictSum(TestCase):
    def test_dict_sum_default(self):
        d1 = {
            1: {
                2: 3
            }
        }
        d2 = {
            1: {
                2: 4
            }
        }
        self.assertEqual(
            zip_dicts(d1, d2),
            {1: {2: (3, 4)}}
        )
        d1 = {
            1: {
                2: 3,
                3: 3,
                4: 2,
            }
        }
        d2 = {
            1: {
                2: 4,
                3: 3,
                4: 3,
            }
        }
        self.assertEqual(
            zip_dicts(d1, d2),
            {1: {2: (3, 4), 4: (2, 3)}}
        )

    def test_dict_sum_with_funcargs(self):
        d1 = {
            1: {
                2: 3,
                3: 3,
                4: 2,
            }
        }
        d2 = {
            1: {
                2: 4,
                3: 3,
                4: 3,
            }
        }
        self.assertEqual(
            zip_dicts(d1, d2, lambda a, b: a+b, lambda a, b: a==b),
            {1: {3: 6}}
        )