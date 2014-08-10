# -*- coding: utf-8 -*-
"""
=============
DrupalLibrary
=============

robotframework keywords and utilities for Drupal testings
"""

import pkg_resources
from robot.api import logger

from .drupalkeywords import DrupalKeywords

# PEP 396 style version marker
try:
    __version__ = pkg_resources.get_distribution(u'robotframework-drupallibrary').version
except:
    logger.warning("Could not get the package version from pkg_resources")
    __version__ = 'unknown'


class DrupalLibrary(DrupalKeywords):
    """=== DrupalLibrary, ATDD testing friend for Drupal sites ===

    Setting up a Drupal site using directly *Selenium2Library* may be a
    hassle.  *DrupalLibrary* provides a set of keyworks for testing Drupal 7
    based sites.

    === About exit_on-failure parameter ===

    You can notice that several keywords like `Sign In` and several others
    take an optional argument named `exit_on_failure` that's ${true} by
    default.

    When such a keyword reports a failure, the test session exits. But you
    could consider that failure as expected. In example, registering a new
    user with `Add Member` will fail for an anonymous user, and the expected
    behaviour is a failure.

    In that kind of test case, you want to carry-on the test suite and
    consider this so called failure as a normal behaviour. You just need to
    add the `exit_on_failure=${false}` parameter to the keyword. In example:

    | Add Member | foo | foo@mydomain | foopassword | exit_on_failure=${false} |
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'
    ROBOT_LIBRARY_VERSION = __version__


