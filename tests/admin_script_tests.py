# tests.admin_script_tests
# Use the subprocess module to execute tribe-admin.py for testing.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jun 22 15:48:08 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin_script_tests.py [6bf9822] benjamin@bengfort.com $

"""
Use the subprocess module to execute tribe-admin.py for testing.
This serves as a form of "integration testing" as well as interface testing.
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest
import subprocess

from . import TEST_VERSION

##########################################################################
## Module Constants and Paths
##########################################################################

PROJECT  = os.path.join(os.path.dirname(__file__), '..')
FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
MBOX     = os.path.join(FIXTURES, "test.mbox")
ADMIN    = os.path.join(PROJECT, "tribe-admin.py")


##########################################################################
## Admin Tests
##########################################################################

class TribeAdminTests(unittest.TestCase):

    def test_paths(self):
        """
        Assert test paths are available.
        """
        for path in (MBOX, ADMIN):
            if not os.path.exists(path):
                self.fail("required file {} does not exist!".format(path))

            if not os.path.isfile(path):
                self.fail("required file {} is not readable!".format(path))

    @unittest.skip("Not python 2.7 compatible for some reason")
    def test_version(self):
        """
        Test that the admin script reports the correct version
        """
        output = subprocess.check_output(["python", ADMIN, "--version"])
        output = output.decode('utf-8')
        self.assertEqual(output, 'tribe v{}\n'.format(TEST_VERSION))
