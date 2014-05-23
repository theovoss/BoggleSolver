#!/usr/bin/env python

"""Test for the command line interface."""


import sys
import unittest
import os.path
import os

from bogglesolver.cli import main


class TestCli(unittest.TestCase):

    """Tests for the cli."""

    def test_main(self):
        """Verify 'bogglesolver' can be called."""
        self.assertIs(None, main([]))

    def test_main_help(self):
        """Verify 'doorstop --help' can be requested."""
        self.assertRaises(SystemExit, main, ['--help'])
        self.assertRaises(SystemExit, main, ['-h'])

    def test_main_solve(self):
        """Verify command line can solve boggle."""
        known_words = ["knife", "mino", "bein", "fink", "nife", "glop", "polk", "mink", "fino", "jink", "nief", "knop", "ink", "fin", "jin", "nim", "kop", "pol", "fab", "fie", "nie", "kon", "lop", "ab", "ef", "if", "mi", "be", "jo", "ch", "on", "lo", "ae", "ea", "in", "ba", "fa", "no", "ko", "op", "po"]
        self.assertIs(known_words, main, ['-s', 'a b c d e f g h i j k l m n o p'])

if __name__ == '__main__':
    unittest.main()