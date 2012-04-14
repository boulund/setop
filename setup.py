#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from distutils.core import setup
import sys

if sys.version_info < (3, 0):
    print("SetOp requires Python 3.")
    sys.exit(1)

import setop

with open("README.rst") as fp:
    readme = fp.read()

setup(name="setop",
      provides=["setop"],
      version=".".join(map(str, setop.__VERSION__)),
      py_modules=["setop"],
      scripts=["scripts/setop"],
      author = "Tigr",
      author_email = "tigr42@centrum.cz",
      url = "https://github.com/tigr42/setop",
      license = "2-clause BSD",
      classifiers = ["Programming Language :: Python",
                     "Programming Language :: Python :: 3",
                     "Development Status :: 3 - Alpha",
                     "Environment :: Console",
                     "Intended Audience :: System Administrators",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Topic :: Text Processing",
                     "Topic :: Text Processing :: Filters",
                     "Operating System :: OS Independent"],
      description="Line-wise set operations on files",
      long_description=readme
    )
