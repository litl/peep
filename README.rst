Peep provides simple but useful tools for Python development.

It includes a reloading function runner that can minimize your
edit-compile-run cycle and some tools for estimating deep memory usage
of objects.

The reloading function runner was inspired by Bret Victor's talk,
"Inventing on Principle". Automatic reexecution is the first step, and
peep may grow to include more functionality from that talk.

Peep is a small API and has no dependencies outside of the Python
standard library. It works with Python 2.6 and 2.7.

Reporting memory usage
======================

It supports getting memory usage (in bytes) of object trees:

::

    >>> obj = {"foo": "bar", "baz": ("quux", "quuux", "quuuux")}
    >>> peep.mem_usage(obj)
    606

The same information, broken down by object type:

::

    >>> obj = {"foo": "bar", "baz": ("quux", "quuux", "quuuux")}
    >>> peep.mem_usage_by_type(obj)
    {<type 'dict'>: 280, <type 'str'>: 246, <type 'tuple'>: 80}


Reloading function runner
=========================

The reloading function runner takes a callable that accepts no
arguments and will not be reloaded itself. This means you can't pass a
reference to an already compiled function; use a partial function or a
lambda expression.

With foo.py:

::

    def run():
        return "This is returned from foo.run()"

::

    >>> import foo
    >>> peep.call_on_change(lambda: foo.run())
    ======== 1365429591.13
    This is returned from foo.run()

    [ modify foo.py ]

    === reloading <module 'foo' from 'foo.py'>
    ======== 1365429594.64
    This is newly returned from foo.run()
