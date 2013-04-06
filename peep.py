# Copyright 2013 litl, LLC. All Rights Reserved
# coding: utf-8

import collections
import gc
import os
import sys
import time
import traceback

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


def call_on_change(callable):
    """Call callable() once, then whenever Python source files are changed

    Print the result after each execution. Catch exceptions and print
    those, too.

    This doesn't yet manage dependencies between loaded modules, so if
    "bar" requires "foo" it will not be reloaded when "foo" is
    changed.

    """
    while 1:
        lastrun = time.time()
        print "========", lastrun
        try:
            print callable()
        except:
            traceback.print_exc()

        # poll until some .pyc file has changed
        while 1:
            restart = False

            for module in filter(_is_py_module, sys.modules.itervalues()):
                if _module_changed_since(lastrun, module):
                    print "=== reloading", module
                    try:
                        reload(module)
                        restart = True
                    except:
                        restart = False
                        lastrun = time.time()
                        traceback.print_exc()
                        continue

            if restart:
                break

            time.sleep(0.5)


def _module_changed_since(since, module):
    filename = getattr(module, "__file__", None)
    if filename and os.path.exists(filename)\
            and _py_changed_since(since, filename):
        return True


def _py_changed_since(since, filename):
    """True if the filename (or associated .py) has been modified"""
    if filename.endswith(".pyc") or filename.endswith(".pyo"):
        filename = filename[:-1]

    return filename.endswith(".py") and os.path.getmtime(filename) > since


def _is_py_module(module):
    """True if the module has been loaded from a .py file"""
    exts = frozenset([".pyc", ".pyo", ".py"])

    filename = getattr(module, "__file__", None)
    return filename and any(filename.endswith(ext) for ext in exts)
