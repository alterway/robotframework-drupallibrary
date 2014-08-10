# -*- coding: utf-8 -*-
"""Misc fixtures and helpers for all tests"""

import functools
import os

tests_directory = os.path.dirname(os.path.abspath(__file__))
tests_abs_path = functools.partial(os.path.join, tests_directory)

from DrupalLibrary import DrupalLibrary

class FakeSelenium2(object):
    pass

class TestingDrupalLibrary(DrupalLibrary):
    def __init__(self, home_url):
        self.home_url = home_url
        self.selenium = FakeSelenium2()

    def go_to(self, location):
        return

