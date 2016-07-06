# tests.stats_tests
# Testing for the stats library in Tribe
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Jul 06 11:34:10 2016 -0400
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt
#
# ID: stats_tests.py [] benjamin@bengfort.com $

"""
Testing for the stats library in Tribe
"""

##########################################################################
## Imports
##########################################################################

import os
import random
import unittest

from tribe.stats import FreqDist

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


##########################################################################
## Helper Functions
##########################################################################

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def random_characters(n, letters=LETTERS):
    for _ in range(n):
        yield random.choice(letters)


##########################################################################
## Frequency Distribution Tests
##########################################################################

class FreqDistTests(unittest.TestCase):

    def test_random_chars(self):
        """
        Assert the random chars generator works.
        """
        data = list(random_characters(100))
        self.assertEqual(len(data), 100)

        for letter in data:
            self.assertIn(letter, LETTERS)

        small = list(random_characters(10, 'abc'))
        self.assertEqual(len(small), 10)

        for letter in small:
            self.assertIn(letter, frozenset(['a', 'b', 'c']))

    def test_n_samples(self):
        """
        Test the computation of N, the number of samples
        """
        dist = FreqDist(random_characters(100))
        self.assertEqual(dist.N, 100)

    def test_memoized_n_samples(self):
        """
        Test the memoization of N, the number of samples
        """
        dist = FreqDist(random_characters(100))
        self.assertEqual(dist.N, 100)

        for letter in random_characters(100):
            dist[letter] += 1

        self.assertEqual(dist.N, 100)
        del dist.N
        self.assertEqual(dist.N, 200)

    def test_b_bins(self):
        """
        Test the computation of B, the number of bins
        """
        dist = FreqDist(random_characters(1000))
        self.assertEqual(dist.B, 26)

    def test_memoized_b_bins(self):
        """
        Test the memoization of B, the number of bins
        """
        dist = FreqDist(random_characters(1000))
        self.assertEqual(dist.B, 26)

        for letter in random_characters(100, 'abcdef'):
            dist[letter] += 1

        self.assertEqual(dist.B, 26)
        del dist.B
        self.assertEqual(dist.B, 32)

    def test_m_magnitude(self):
        """
        Test the computation of M, the magnitude
        """
        dist = FreqDist('aaabbbaaabccddeeffbbccddeegjja')
        self.assertEqual(dist.M, 7)

    def test_memoized_m_magnitude(self):
        """
        Test the memoization of M, the magnitude
        """
        dist = FreqDist('aaabbbaaabccddeeffbbccddeegjja')
        self.assertEqual(dist.M, 7)

        for letter in 'aaabbccc':
            dist[letter] += 1

        self.assertEqual(dist.M, 7)
        del dist.M
        self.assertEqual(dist.M, 10)

    def test_freq(self):
        """
        Test the computation of the frequency
        """
        samples = list(random_characters(90, 'abc'))
        samples.extend(['d']*10)
        dist = FreqDist(samples)

        self.assertEqual(dist.N, len(samples))
        self.assertEqual(dist.B, 4)
        self.assertAlmostEqual(dist.freq('d'), 0.1)

        for c in 'abc':
            self.assertGreater(dist.freq(c), 0.0)
            self.assertLess(dist.freq(c), 1.0)

    def test_empty_freq(self):
        """
        Test the frequency of an empty distribution
        """
        dist = FreqDist()
        self.assertEqual(dist.freq('a'), 0)

    def test_norm(self):
        """
        Test the computation of the norm
        """
        samples = list(random_characters(50, 'abc'))
        samples.extend(['d']*50)
        dist = FreqDist(samples)

        self.assertEqual(dist.max(), 'd')
        self.assertEqual(dist.N, len(samples))
        self.assertEqual(dist.M, 50)
        self.assertAlmostEqual(dist.norm('d'), 1.0)

        for c in 'abc':
            self.assertGreater(dist.norm(c), 0.0)
            self.assertLess(dist.norm(c), 1.0)

    def test_empty_norm(self):
        """
        Test the norm of an empty distribution
        """
        dist = FreqDist()
        self.assertEqual(dist.norm('a'), 0)

    def test_max(self):
        """
        Test maximal element selection
        """
        dist = FreqDist('aaabbbaaabccddeeffbbccddeegjja')
        self.assertEqual(dist.max(), 'a')

    def test_empty_max(self):
        """
        Test the frequency of an empty distribution
        """
        dist = FreqDist()
        self.assertIsNone(dist.max())

    def test_ratio(self):
        """
        Test the ratio computation
        """
        dist = FreqDist('aaabbbaaabccddeeffbbccddeegjja')
        self.assertAlmostEqual(dist.ratio('a', 'b'), 1.16666667)
        self.assertAlmostEqual(dist.ratio('b', 'a'), 0.85714285)

    def test_missing_ratio(self):
        """
        Test that ratio of an unseen element is 0
        """
        dist = FreqDist(random_characters(100, 'abc'))
        self.assertEqual(dist.ratio('a', 'd'), 0)

    def test_inverse_ratio(self):
        """
        Test that the ratio is correct for the inverse
        """
        dist = FreqDist(random_characters(1000, 'abc'))
        rtab = dist.ratio('a', 'b')
        rtba = dist.ratio('b', 'a')

        riab = 1.0 / rtab
        riba = 1.0 / rtba

        self.assertAlmostEqual(riab, rtba)
        self.assertAlmostEqual(riba, rtab)

    def test_str(self):
        """
        Test the stringification of the frequency distribution
        """
        try:
            dist = FreqDist(random_characters(1000, 'abc'))
            s = str(dist)
            r = repr(dist)
            p = dist.pprint()
        except Exception as e:
            self.fail("Stringifcation failed: {}".format(e))

    def test_dump_and_load(self):
        """
        Test the serialization of frequency distribution
        """
        fobj = StringIO()
        orig = FreqDist(random_characters(1000))

        # Dump the frequncy distribution to the stream
        orig.dump(fobj)

        # Seek to 0 and load the frequency distribution
        fobj.seek(0)
        dist = FreqDist.load(fobj)

        self.assertEqual(orig, dist)
