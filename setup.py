#!/usr/bin/env python
# coding: utf-8

import peep

# Require setuptools. See http://pypi.python.org/pypi/setuptools for
# installation instructions, or run the ez_setup script found at
# http://peak.telecommunity.com/dist/ez_setup.py
from setuptools import setup

# Load the test requirements. These are in a separate file so they can
# be accessed from Travis CI and tox.
with open("test-requirements.txt") as fd:
    tests_require = list(fd.xreadlines())


setup(
    name="peep",
    version=peep.__version__,
    author="Peter Teichman",
    author_email="pteichman@litl.com",
    license="MIT",
    url="https://github.com/litl/peep",
    description="Simple but useful development tools for Python",
    py_modules=["peep"],

    setup_requires=[
        "unittest2==0.5.1"
    ],

    test_suite="unittest2.collector",
    tests_require=tests_require,

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ]
)
