#!/usr/bin/env python

"""Test for the command line interface."""


import unittest

from bogglesolver.cli import main


class TestCli(unittest.TestCase):

    """Tests for the cli."""

    def test_main(self):
        """Verify 'bogglesolver' can be called."""
        self.assertIs(None, main([]))

    def test_main_help(self):
        """Verify 'bogglesolver --help' can be requested."""
        self.assertRaises(SystemExit, main, ['--help'])
        self.assertRaises(SystemExit, main, ['-h'])

if __name__ == '__main__':
    unittest.main()
