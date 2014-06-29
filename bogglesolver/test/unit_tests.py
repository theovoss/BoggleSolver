#!/usr/bin/env python

"""Unit tests for all boggle classes."""


import unittest

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle

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


class test_boggle_adjacent(unittest.TestCase):

    """Unit tests for testing which indices are adjacent in different board configurations."""

    def test_four_by_four(self):
        """Test a 4x4 board adjacency."""
        game = Boggle(4, 4)
        assert game.is_adjacent(0, 1)
        assert game.is_adjacent(1, 2)
        assert game.is_adjacent(2, 3)
        assert False is game.is_adjacent(3, 4)
        assert False is game.is_adjacent(3, 5)
        assert False is game.is_adjacent(3, 11)
        assert game.is_adjacent(4, 5)
        assert game.is_adjacent(6, 7)
        assert game.is_adjacent(8, 9)
        assert game.is_adjacent(10, 11)
        assert game.is_adjacent(12, 13)
        assert game.is_adjacent(14, 15)
        assert game.is_adjacent(1, 1)
        assert game.is_adjacent(5, 10)
        assert game.is_adjacent(1, 4)

    def test_five_by_three(self):
        """Test a 5x3 board adjacency."""
        game = Boggle(5, 3)
        assert game.is_adjacent(0, 1)
        assert game.is_adjacent(6, 7)
        assert game.is_adjacent(12, 13)
        assert game.is_adjacent(0, 7) is False
        assert game.is_adjacent(3, 13) is False
        assert game.is_adjacent(0, 14) is False
        assert game.is_adjacent(1, 7)
        assert game.is_adjacent(9, 13)
        assert game.is_adjacent(4, 8)

    def test_get_adjacent53(self):
        """Test a 5x3 board adjacency."""
        game = Boggle(5, 3)
        # middle
        adj = game.get_adjacent(6)
        expected = [0, 1, 2, 5, 7, 10, 11, 12]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # middle - except some already visited
        adj = game.get_adjacent(6, [0, 1, 7, 11])
        expected = [2, 5, 10, 12]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # side
        adj = game.get_adjacent(9)
        expected = [3, 4, 8, 13, 14]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # side - except some already visited
        adj = game.get_adjacent(9, [4, 13, 1])
        expected = [3, 8, 14]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # corner
        adj = game.get_adjacent(0)
        expected = [1, 5, 6]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # corner - except some already visited
        adj = game.get_adjacent(0, [5, 4, 9])
        expected = [1, 6]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # test unnormal adjacent
        adj = game.get_adjacent(0, normal_adj=False)
        for index in range(1, len(game.boggle_array) - 2):
            assert index in adj
        assert len(adj) == len(game.boggle_array) - 1

    def test_get_adjacent44(self):
        """Test a 4x4 board adjacency."""
        game = Boggle(4, 4)

        # middle
        adj = game.get_adjacent(6)
        expected = [1, 2, 3, 5, 7, 9, 10, 11]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # middle - except some already visited
        adj = game.get_adjacent(6, [2, 4, 6, 10])
        expected = [1, 3, 5, 7, 9, 11]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # side
        adj = game.get_adjacent(7)
        expected = [2, 3, 6, 10, 11]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # side - except some already visited
        adj = game.get_adjacent(7, [3, 10, 20, 500])
        expected = [2, 6, 11]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # corner
        adj = game.get_adjacent(12)
        expected = [8, 9, 13]
        for index in expected:
            assert index in adj
        assert len(adj) is len(expected)

        # corner - except some already visited
        adj = game.get_adjacent(12, [8, 9, 13])
        assert len(adj) is 0


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

if __name__ == '__main__':
    unittest.main()
