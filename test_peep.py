# Copyright 2013 litl, LLC. All Rights Reserved.
# coding: utf-8

import peep
import types
import unittest2 as unittest


def iterlen(iterable):
    return sum(1 for _ in iterable)


class MemoryTest(unittest.TestCase):
    def test_visit_referents(self):
        # Test the count of objects visited from a variety of data structures

        # 1 object: the empty list
        obj = []
        self.assertEqual(1, iterlen(peep._visit_referents(obj)))

        # 2 objects: the list and None
        obj = [None]
        self.assertEqual(2, iterlen(peep._visit_referents(obj)))

        # 2 objects: the list and None (the second None is not visited)
        obj = [None, None]
        self.assertEqual(2, iterlen(peep._visit_referents(obj)))

        # 2 objects: the tuple and None
        obj = (None, None)
        self.assertEqual(2, iterlen(peep._visit_referents(obj)))

        # 3 objects: the dict, its key, and its value
        obj = {"foo": "bar"}
        self.assertEqual(3, iterlen(peep._visit_referents(obj)))

        # 3 objects: the set and both items
        obj = set(["foo", "bar"])
        self.assertEqual(3, iterlen(peep._visit_referents(obj)))

        # Construct a dict with two items referring to the same objects
        foo, bar = "foo", "bar"
        obj = {foo: bar, bar: foo}
        self.assertEqual(3, iterlen(peep._visit_referents(obj)))

    def test_relative_mem_usage(self):
        # Actual bytes reported from mem_usage will depend on the
        # Python runtime used, and could conceivably vary from run to
        # run, with e.g. hash randomization. So these tests are mostly
        # relative.

        # This is a list of tuples where the first object should be
        # smaller (in mem_usage) than the second.
        tests = [
            ("foo", "fooo"),
            ("foo", ["foo"]),
            (["foo"], ["fooo"]),
            (set("foo"), set(["foo", "bar"])),
        ]

        for index, test in enumerate(tests):
            obj1, obj2 = test
            self.assertGreater(peep.mem_usage(obj2), peep.mem_usage(obj1),
                               "failed at test #%d" % index)

    def test_mem_usage_by_type(self):
        obj = [1, 2, 3, 4, (1, 2), "foo", "bar"]
        tests = (types.IntType, types.ListType, types.StringType,
                 types.TupleType)

        usage = peep.mem_usage_by_type(obj)

        for index, test in enumerate(tests):
            self.assertIn(test, usage, "failed at test #%d" % index)
