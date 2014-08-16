#!/usr/bin/env python

"""Unit tests for all boggle classes."""


import unittest

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle

from bogglesolver.twl06 import TEST_WORD_LIST


class test_boggle_letters(unittest.TestCase):

    """Unit tests for adding letters to the boggle board."""

    def test_str(self):
        """Test converting to string works."""
        game = Boggle(4, 4)
        assert str(game) == ""
        game.boggle_array = ['A'] * 4 + ['B'] * 4 + ['C'] * 4 + ['D'] * 4
        assert str(game) == " | A | A | A | A |\n | B | B | B | B |\n | C | C | C | C |\n | D | D | D | D |\n"

    def test_insert_index(self):
        """Test inserting a character into the boggle array."""
        game = Boggle(4, 4)
        game.insert('A', 0)
        assert game.boggle_array[0] is 'A'

        game.insert('B', 8)
        assert game.boggle_array[8] is 'B'

    def test_boggle_is_full(self):
        """Test that boggle array is full."""
        game = Boggle(4, 4)
        assert game.is_full() is False

        for i in range(0, 16):
            game.insert('A', i)
        assert game.is_full()

    def test_boggle_set_array(self):
        """Test that the boggle array can be set."""
        game = Boggle(4, 4)
        assert game.is_full() is False
        array = ["a"] * 16
        game.set_array(array)
        assert game.is_full()


class test_dictionary(unittest.TestCase):

    """Unit tests for the dictionary."""

    def test_hi(self):
        """Test adding a word."""
        my_dict = Edict()
        my_dict.add_word("hi")
        assert my_dict.is_word("hi")

    def test_casesensetive(self):
        """Test that dictionary is not case sensetive."""
        my_dict = Edict()
        my_dict.add_word("ThEoDoRe")
        assert my_dict.is_word("theodore")
        assert my_dict.is_word("THEODORE")
        assert my_dict.is_word("THEOdore")

    def test_multiplewordswithsameroot(self):
        """Test that the dict handles words with the same root."""
        my_dict = Edict()
        my_dict.add_word("he")
        my_dict.add_word("HELL")
        my_dict.add_word("HELLo")
        assert my_dict.is_word("he")
        assert my_dict.is_word("hell")
        assert my_dict.is_word("hello")
        assert False is my_dict.is_word("h")
        assert False is my_dict.is_word("hel")

    def test_is_still_valid(self):
        """Test for valid dictionary paths."""
        my_dict = Edict()
        my_dict.read_dictionary(True)
        assert my_dict.is_still_potentially_valid("ortho")
        assert my_dict.is_still_potentially_valid("orthorhombic")
        assert my_dict.is_still_potentially_valid("orthorhombics") is False
        assert my_dict.is_still_potentially_valid("1") is False
        assert my_dict.is_still_potentially_valid("aa")
        assert my_dict.is_still_potentially_valid("A")
        assert my_dict.is_still_potentially_valid("AaA") is False

    def test_get_words(self):
        """Test getting words out of the dictionary."""
        my_dict = Edict()
        my_dict.read_dictionary(True)
        words = my_dict.get_words(my_dict.dictionary_root)
        print(words)
        dict_words = TEST_WORD_LIST
        for word in dict_words:
            print(word)
            assert word.lower() in words
        assert len(words) is len(dict_words)

    def test_get_last_node(self):
        """Test valid paths in the dictionary."""
        my_dict = Edict()
        my_dict.read_dictionary(True)
        assert my_dict.get_last_node(my_dict.dictionary_root, 'o')
        assert my_dict.get_last_node(my_dict.dictionary_root.letters['o'], 'b') is None


class test_SolveMultiLetterBoggle(unittest.TestCase):

    """Unit tests for multi-letter solve game."""

    def test_MultiLetterBoard(self):
        """Test multi-letter."""
        rows = 1
        array = ["w", "at", "e", "r"]
        word = "water"
        solve_game = SolveBoggle(True)
        solve_game.set_board(4, rows, array)
        words = solve_game.solve()
        print(words)
        assert word in words
        assert len(words) == 1

        array = ["wa", "te", "r"]
        solve_game.set_board(3, rows, array)
        words = solve_game.solve()
        print(words)
        assert word in words
        assert len(words) == 1

        array = ["wat", "er"]
        solve_game.set_board(2, rows, array)
        words = solve_game.solve()
        print(words)
        assert word in words
        assert len(words) == 1

        array = ["water"]
        solve_game.set_board(1, rows, array)
        words = solve_game.solve()
        print(words)
        assert word in words
        assert len(words) == 1


class test_SolveBoggle(unittest.TestCase):

    """Unit tests for solve boggle."""

    def test_set_board(self):
        """Test set_board."""
        columns = 10
        rows = 1
        array = ["w", "a", "t", "e", "r"]
        array2 = ["w", "a", "t", "e", "r", "w", "a", "t", "e", "r"]
        solve_game = SolveBoggle(True)

        assert not solve_game.boggle.is_full()
        assert solve_game.boggle.num_rows != rows
        assert solve_game.boggle.num_columns != columns

        solve_game.set_board(columns, rows, array)

        assert not solve_game.boggle.is_full()
        assert solve_game.boggle.num_rows == rows
        assert solve_game.boggle.num_columns == columns

        solve_game.set_board(columns, rows, array2)

        assert solve_game.boggle.is_full()
        assert solve_game.boggle.num_rows == rows
        assert solve_game.boggle.num_columns == columns


if __name__ == '__main__':
    unittest.main()
