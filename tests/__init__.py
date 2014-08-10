# -*- coding: utf-8 -*-
"""\
=============
DrupalLibrary
=============

Tests package
"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from .resources import tests_directory

def all_tests():
    return unittest.defaultTestLoader.discover(tests_directory)
