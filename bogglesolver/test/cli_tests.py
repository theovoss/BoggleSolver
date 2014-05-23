#!/usr/bin/env python

"""Test for the command line interface."""


import sys
import unittest
import os.path
import os

from bogglesolver.cli import main


class TestCli(unittest.TestCase):

    """Tests for the cli."""

    def test_main_help(self):
        """Verify 'bogglesolver --help' can be requested."""
        # self.assertRaises(SystemExit, main, ['--help'])
        print("printing main")
        print(main, '--help')
        assert(False)

if __name__ == '__main__':
    unittest.main()