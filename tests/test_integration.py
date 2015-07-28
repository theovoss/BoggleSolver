#!/usr/bin/env python
# pylint: disable=R0201
"""Integration tests for all boggle classes."""


import unittest

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle
from bogglesolver.adjacency import get_scrabble_adjacent

from bogglesolver.twl06 import WORD_LIST


class TestSolveBoggle(unittest.TestCase):

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


class TestEverything(unittest.TestCase):

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

    def test_solves_boggle(self):
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
        my_dict = Edict()
        my_dict.read_dictionary()

        for line in WORD_LIST:
            my_dict.is_word(line.lower())
            assert my_dict.is_word(line.lower())

if __name__ == '__main__':
    unittest.main()
