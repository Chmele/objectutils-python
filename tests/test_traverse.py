from objectutils import traverse, PathGroup as pg
from unittest import TestCase


class TestTraverseSingleDispatch(TestCase):
    def test_traverse_dict_pathgroup(self):
        self.assertListEqual(
            traverse({1: {4: 1}, 2: {3: {4: 4}, 5: 5}}, [pg([1, 4], [2, 3])]),
            [1, {4: 4}]
        )

    def test_traverse_dict_anykey(self):
        self.assertListEqual(
            traverse({1: {4: 1}, 2: {3: {4: 4}, 5: {4: 4}}}, [2, [], 4]),
            [4, 4]
        )

    def test_traverse_list(self):
        self.assertEqual(
            traverse([1, 2, [1, 2, [1, 2]]], [2, 2, 1]),
            2
        )
    
    def test_dict_traverse_trivial(self):
        a = {1:{}, 2: {3: 4, 5: 6, 7: 8}}
        self.assertEqual(
            traverse(a, [2, 3]),
            4
        )

        self.assertEqual(
            traverse(a, []),
            a
        )

        with self.assertRaises(KeyError):
            traverse(a, [1, 0])

    def test_list_traverse_trivial(self):
        a = [[], [1], [1, 2]]
        self.assertEqual(
            traverse(a, [2, 1]),
            2
        )

        self.assertEqual(
            traverse(a, []),
            a
        )
        with self.assertRaises(IndexError):
            traverse(a, [1, 1])

        with self.assertRaises(TypeError):
            traverse(a, [1, 0, 0])

    def test_function_call(self):
        a = {1: {4: 1}, 2: {3: {4: 4}, 5: 5, 6: 6}}
        self.assertEqual(
            traverse(a, [sum, pg([1, 4], [2, 5])]),
            6
        )

        self.assertEqual(
            traverse(a, [sum, 2, pg([5], [6])]),
            11
        )

    def test_class_call(self):
        a = {"computers": 
            [
                {
                    "computername": "1",
                    "software": ["s1", "s2"],
                },
                {
                    "computername": "2",
                    "software": ["s2", "s3"],
                },
                {
                    "computername": "3",
                    "software": ["s1", "s3"],
                },
            ]
        }
        from collections import Counter
        from itertools import chain
        self.assertEqual(
            traverse(a, [Counter, chain.from_iterable, "computers", [], "software"]),
            {"s1": 2, "s2": 2, "s3": 2}
        )

    def test_fallback_call(self):
        a = {1: [1,2,3,4]}
        self.assertEqual(
            traverse(a, [lambda *args: sum(args), 1]),
            10
        )
        self.assertEqual(
            traverse(a, [lambda a: sum(a), 1]),
            10
        )

    def test_dict_item(self):
        self.assertEqual(traverse({1:{2:3}}, [{2:[1]}]), {2:{2:3}})
        self.assertEqual(traverse({1: {2: 3}}, [{2: [1], 3: [1, 2]}]), {2: {2: 3}, 3: 3})
        self.assertEqual(traverse({1:{2:3}}, [ {2:[]}, {3:[]}, 1, 2]), {2: {3: 3}})
        self.assertEqual(traverse({1:{2:3}, 4: 5}, [ {2:[]}, [{3:[1, 2]}, {"4":[4]}]]), {2: [{3: 3}, {'4': 5}]})
