#!/usr/bin/env python

"""Integration tests for all boggle classes."""


import sys
import unittest
import os.path
import time
import sqlite3
import os

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle
from bogglesolver.adjacency import *

from bogglesolver.twl06 import WORD_LIST
from bogglesolver.twl06 import TEST_WORD_LIST


class test_solve_boggle(unittest.TestCase):

    """Unit tests for the solve boggle class."""

    def test_init(self):
        """Test solve boggle."""
        columns = 5
        rows = 1
        array = ["w", "a", "t", "e", "r"]
        solve_game = SolveBoggle(True)
        edict = Edict()
        solve_game.set_board(columns, rows, array)
        edict.add_word("wata")
        edict.add_word("wate")
        edict.add_word("water")
        edict.add_word("a")
        edict.add_word("tear")
        edict.add_word("tea")
        edict.add_word("eat")
        solved = solve_game.solve(edict)
        assert "water" in solved
        assert "a" not in solved
        assert "wata" not in solved
        assert "wate" in solved
        assert "eat" not in solved
        assert "tear" not in solved
        assert "tea" not in solved

        solve_game.min_word_len = 0
        solved = solve_game.solve(edict)
        assert "a" in solved

        solved = solve_game.solve(edict, adjacency_funct=get_scrabble_adjacent)
        assert "water" in solved
        assert "a" in solved
        assert "wata" not in solved
        assert "wate" in solved
        assert "eat" in solved
        assert "tea" in solved
        assert "tear" in solved

        solve_game = SolveBoggle(True)
        solve_game.set_board(columns, rows, None)
        print("Columns are: %s, Rows are: %s" % (columns, rows))
        assert solve_game.boggle.is_full()


class test_everything(unittest.TestCase):

    """
    All integration Tests.

    These tests all take a somewhat significant amount of time, usually due to loading in the dictionary.
    Could speed these up a lot if I store that dictionary globally.
    """

    def test_generate_board(self):
        """Test generating the board."""
        game = Boggle(4, 4)
        game.generate_boggle_board()
        assert game.is_full()

    def test_solves_Boggle(self):
        """Test solving the boggle board."""
        columns = 4
        rows = 4
        array = "a b c d e f g h i j k l m n o p".split()

        assert len(array) == columns * rows

        solve_game = SolveBoggle()
        solve_game.set_board(columns, rows, array)
        edict = Edict()

        # found words from: http://www.bogglecheat.net/, though may not be in my dictionary
        known_words = ["knife", "mino", "bein", "fink", "nife", "glop", "polk", "mink", "fino", "jink", "nief", "knop", "ink", "fin", "jin", "nim", "kop", "pol", "fab", "fie", "nie", "kon", "lop", "ab", "ef", "if", "mi", "be", "jo", "ch", "on", "lo", "ae", "ea", "in", "ba", "fa", "no", "ko", "op", "po"]
        for word in known_words:
            edict.add_word(word)

        solve_game.min_word_len = 5
        solved = solve_game.solve(edict)

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

        solve_game.min_word_len = 0
        solved = solve_game.solve(edict)

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

    def test_loads_all_words(self):
        """Test the dictionary can load all the words."""
        t0 = time.time()
        my_dict = Edict()
        my_dict.read_dictionary()
        t1 = time.time()

        for line in WORD_LIST:
            my_dict.is_word(line.lower())
            assert my_dict.is_word(line.lower())


class test_speed_against_other_libraries(unittest.TestCase):

    """Test my boggle library against other boggle libraries."""

    @unittest.skip("Skipping library comparisons.")
    def test_pypi_init_speeds(self):
        """Test how fast they load."""
        import boggleboard

        other_default_size = 4
        letters = ['i', 'r', 'e', 'e', 'r', 'i', 'u', 'c', 't', 's', 'i', 'e', 'a', 'n', 'i', 'a']

        t1 = time.time()
        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)
        t2 = time.time()

        their_time = t2 - t1

        t1 = time.time()
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t2 = time.time()

        my_time = t2 - t1

        print("My init time is: %s" % my_time)
        print("Their init time is: %s" % their_time)
        print("Mine is %s slower." % (my_time / their_time))
        assert my_time / their_time < 2

    @unittest.skip("Skipping library comparisons.")
    def test_pypi_4_by_4(self):
        """Test 4x4 against the current boggle board on pypi."""
        import boggleboard
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e',
                   'r', 'i', 'u', 'c',
                   't', 's', 'i', 'e',
                   'a', 'n', 'i', 'a']

        edict = Edict()

        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)

        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()

        their_solve_time = t2 - t1

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve(edict)
        t2 = time.time()

        my_solve_time = t2 - t1

        time_difference = my_solve_time / their_solve_time

        print("I found %s words." % len(my_words))
        print("They found %s words." % len(their_words))
        print("Mine is %s percent slower" % time_difference)
        print("My total time %s\nTheir total time %s" % (my_solve_time, their_solve_time))

        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                assert my_boggle.edict.is_word(word)
        for word in my_words:
            assert word in their_words
        assert len(my_words) == len(their_words)
        assert time_difference < 1
        assert False

    @unittest.skip("Skipping library comparisons.")
    def test_pypi_10_by_10(self):
        """Test 10x10 against the current boggle board on pypi."""
        import boggleboard

        edict = Edict()

        other_default_size = 10
        letters = ['o', 'i', 's', 'r', 'l', 'm', 'i', 'e', 'a', 't',
                   'g', 'e', 't', 'y', 'r', 'b', 'd', 's', 's', 'h',
                   'f', 'r', 'h', 'r', 'a', 'e', 'd', 'g', 'l', 'u',
                   'e', 'i', 'e', 'r', 's', 's', 'o', 'n', 'o', 'a',
                   'o', 'd', 'e', 'g', 'a', 'o', 'e', 't', 's', 'm',
                   'e', 'y', 's', 'e', 'e', 'b', 'i', 'd', 't', 'h',
                   'y', 'm', 'i', 'r', 'p', 'c', 's', 'm', 'r', 'e',
                   'b', 't', 'o', 'o', 'e', 'i', 'p', 's', 'r', 'u',
                   's', 'l', 'w', 'o', 'k', 'l', 'c', 't', 's', 'l',
                   'n', 'l', 'r', 'r', 'e', 'i', 'e', 's', 'g', 't']

        their_boggle = boggleboard.BoggleBoard(other_default_size, letters)
        their_trie = boggleboard.Trie(WORD_LIST)

        t1 = time.time()
        their_words = their_boggle.findWords(their_trie)
        t2 = time.time()

        their_solve_time = t2 - t1

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve(edict)
        t2 = time.time()

        my_solve_time = t2 - t1

        time_difference = my_solve_time / their_solve_time

        print("I found %s words." % len(my_words))
        print("They found %s words." % len(their_words))

        print("Mine is %s percent slower" % time_difference)
        print("My total time %s\nTheir total time %s" % (my_solve_time, their_solve_time))
        for word in their_words:
            if word not in my_words:
                print("I didn't find: %s" % word)
                assert my_boggle.edict.is_word(word)
        for word in my_words:
            assert word in their_words
        assert len(my_words) == len(their_words)
        assert time_difference < 1
        assert False

    @unittest.skip("Skipping library comparisons.")
    def test_100x100_time(self):
        """Test 100x100 against the current boggle board on pypi."""
        import boggleboard
        edict = Edict()
        other_default_size = 100
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size)

        t1 = time.time()
        my_words = my_boggle.solve(edict)
        t2 = time.time()

        my_solve_time = t2 - t1

        print("Found %s words." % len(my_words))
        print("Took %s seconds to solve 100x100." % my_solve_time)

        # make sure we can solve 100x100 in a reasonable ammount of time.
        assert my_solve_time < 120
        assert False


if __name__ == '__main__':
    unittest.main()
