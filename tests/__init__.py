# tests
# Testing for the tribe module
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Nov 12 20:42:42 2014 -0500
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Testing for the tribe module
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTests(unittest.TestCase):

    def test_initialization(self):
        """
        Test that the world is sane and 2+2=4
        """
        self.assertEqual(2+2,4)

    def test_import(self):
        """
        Check ability to import the tribe module
        """
        try:
            import tribe
        except ImportError:
            self.fail("Could not import the tribe module")
