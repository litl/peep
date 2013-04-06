# Copyright 2013 litl, LLC. All Rights Reserved
# coding: utf-8

import collections
import gc
import sys

__version__ = "0.9.0"


def _visit_referents(root):
    """Yield the objects reachable from obj

    This yields each object once, in no particular order.

    """
    seen = set()
    left = collections.deque([root])

    while left:
        obj = left.popleft()
        if id(obj) in seen:
            continue

        yield obj

        seen.add(id(obj))
        for child in gc.get_referents(obj):
            left.append(child)


def mem_usage(obj):
    """Sum the bytes used by obj and any object reachable from obj

    >>> peep.mem_usage([1, 2, 3, 4])
    200

    """
    return sum(sys.getsizeof(o) for o in _visit_referents(obj))


def mem_usage_by_type(obj):
    """Aggregate the memory usage of objects reachable from obj (by type)

    >>> peep.mem_usage_by_type([1, 2, 3, 4, (1, 2)])
    {<type 'list'>: 112, <type 'tuple'>: 72, <type 'int'>: 24}

    """
    # This would use a collections.Counter(), but that doesn't exist
    # in 2.6.  You can always collections.Counter(result) on 2.7 if
    # you want its methods.
    counts = collections.defaultdict(int)

    for o in _visit_referents(obj):
        counts[type(o)] += sys.getsizeof(o)

    return counts
