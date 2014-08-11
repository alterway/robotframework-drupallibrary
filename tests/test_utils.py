# -*- coding: utf-8 -*-
"""
=================
Utilities testing
=================

Utilities don't need complicated fixtures, and are tested independently
"""

import unittest

from DrupalLibrary.drupalkeywords import  FailureManager


class FailureManagerTest(unittest.TestCase):
    """Testing FailureManager context manager"""
    def test_no_exception(self):
        """When no exception occurs all's as usual"""
        with FailureManager(False):
            dummy = 0

        # Since we should execute this. Seems idiot but...
        self.assertEqual(dummy, 0)

    def test_non_critical(self):
        """We don't consider an exception as critical"""
        with self.assertRaises(Exception) as assertion:
            with FailureManager(False, "reason"):
                raise Exception("eek")

        exc = assertion.exception
        self.assertTrue(exc.message.startswith("eek"))
        self.assertTrue(exc.message.endswith("reason"))
        self.assertFalse(hasattr(exc, 'ROBOT_EXIT_ON_FAILURE'))

    def test_critical(self):
        """This exception should propagate and stop the tests run"""
        with self.assertRaises(Exception) as assertion:
            with FailureManager(True, "reason"):
                raise Exception(("eek"))
        exc = assertion.exception
        self.assertTrue(exc.message.startswith("eek"))
        self.assertTrue(exc.message.endswith("reason"))
        self.assertTrue(getattr(exc, 'ROBOT_EXIT_ON_FAILURE'))
