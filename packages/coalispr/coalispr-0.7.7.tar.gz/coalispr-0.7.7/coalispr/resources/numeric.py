#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pandas/core/indexes/numeric.py

from pandas.core.indexes.base import Index

""" A set of classes to enable python.shelve to deal with pickled databases on
pandas-2. See:

https://github.com/pandas-dev/pandas/issues/53300
https://github.com/pandas-dev/pandas/issues/53300#issuecomment-1553939190
"""

class NumericIndex(Index):
    pass

class IntegerIndex(NumericIndex):
    pass

class Int64Index(IntegerIndex):
    pass

class UInt64Index(IntegerIndex):
    pass

class Float64Index(NumericIndex):
    pass
