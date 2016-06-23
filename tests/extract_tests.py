# tests.extract_tests
# Test the tribe extraction module
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jun 22 16:40:26 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: extract_tests.py [cc23aed] benjamin@bengfort.com $

"""
Test the tribe extraction module
"""

##########################################################################
## Imports
##########################################################################

import os
import json
import unittest
import networkx as nx

from datetime import datetime
from tribe.extract import MBoxReader
from tribe.emails import EmailMeta, EmailAddress
from six import string_types

##########################################################################
## Fixtures
##########################################################################

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
MBOX     = os.path.join(FIXTURES, "test.mbox")
HEADERS  = os.path.join(FIXTURES, "headers.json")

class MBoxReaderTests(unittest.TestCase):
    """
    Testing the mbox reader for email extraction.
    """

    def setUp(self):
        self.reader = MBoxReader(MBOX)

    def tearDown(self):
        self.reader = None

    def test_header_analysis(self):
        """
        Test the header analysis functionality
        """
        headers  = self.reader.header_analysis()
        self.assertEqual(len(headers), 25)

        with open(HEADERS, 'r') as f:
            expected = json.load(f)

        for header, count in expected.items():
            self.assertEqual(count, headers[header])

    def test_count(self):
        """
        Test that the number of emails is expected
        """
        self.assertEqual(self.reader.count(), 140)
        self.assertEqual(self.reader.count(), len(self.reader))

    def test_extract(self):
        """
        Make sure that extract does not error
        """
        for idx, msg in enumerate(self.reader.extract()):

            # Some simple type checking
            self.assertIsInstance(msg, EmailMeta)
            self.assertIsInstance(msg.sender, EmailAddress)
            self.assertIsInstance(msg.recipients, list)
            self.assertIsInstance(msg.copied, list)
            self.assertIsInstance(msg.subject, string_types + (None,))
            self.assertIsInstance(msg.date, (datetime, None))

        self.assertEqual(idx+1, 140)

    def test_graph_extract(self):
        """
        Make sure that extract graph does not error
        """
        G = self.reader.extract_graph()
        self.assertEqual(nx.number_of_nodes(G), 7)
        self.assertEqual(nx.number_of_edges(G), 6)
        self.assertFalse(nx.is_directed(G))
