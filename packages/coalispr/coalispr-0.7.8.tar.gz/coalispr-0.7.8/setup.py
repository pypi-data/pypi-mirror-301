#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#
#  Copyright 2020-2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#

from setuptools import setup
#from Cython.Build import cythonize
#import numpy

setup(
#    ext_modules=cythonize(
#        "coalispr/bedgraph_analyze/*.pyx",
#        compiler_directives={"language_level": "3"},
#        annotate=True
#        ),
#    include_dirs=[numpy.get_include()]
    )

## run in terminal
## include dot at end, meaning 'current directory'
#pip3 install --editable .
## or,
#python3 -m pip install --editable .
