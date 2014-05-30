#!/usr/bin/env python

"""Unit tests for all boggle classes."""


import unittest
import os
import subprocess
import re

from bogglesolver.load_english_dictionary import e_dict
from bogglesolver.boggle_board import boggle
from bogglesolver.solve_boggle import solve_boggle

from bogglesolver.twl06 import test_word_list


class test_boggle_letters(unittest.TestCase):

    """Unit tests for adding letters to the boggle board."""

    def test_print_board(self):
        b = boggle(4, 4)
        array = "a b c d e f g h i j k l m n o p".split(' ')
        expected_string = " | a | b | c | d |\n | e | f | g | h |\n | i | j | k | l |\n | m | n | o | p |\n"
        b.set_array(array)
        assert b.__str__() == expected_string

    def test_insert_index(self):
        b = boggle(4, 4)
        b.insert('A', 0)
        assert b.boggle_array[0] is 'A'

        b.insert('B', 8)
        assert b.boggle_array[8] is 'B'

    def test_boggle_is_full(self):
        b = boggle(4, 4)
        assert b.is_full() is False

        for i in range(0, 16):
            b.insert('A', i)
        assert b.is_full()

    def test_boggle_set_array(self):
        b = boggle(4, 4)
        assert b.is_full() is False
        array = ["a"] * 16
        b.set_array(array)
        assert b.is_full()


class test_boggle_adjacent(unittest.TestCase):

    """Unit tests for testing which indices are adjacent in different board configurations."""

    def test_boggle_board_generate(self):
        b = boggle(4, 4)
        assert False is b.is_full()
        b.generate_boggle_board()
        assert b.is_full()
        for letter in b.boggle_array:
            assert re.search('[a-z]', letter) is not None

    def test_four_by_four(self):
        b = boggle(4, 4)
        assert b.is_adjacent(0, 1)
        assert b.is_adjacent(1, 2)
        assert b.is_adjacent(2, 3)
        assert False is b.is_adjacent(3, 4)
        assert False is b.is_adjacent(3, 5)
        assert False is b.is_adjacent(3, 11)
        assert b.is_adjacent(4, 5)
        assert b.is_adjacent(6, 7)
        assert b.is_adjacent(8, 9)
        assert b.is_adjacent(10, 11)
        assert b.is_adjacent(12, 13)
        assert b.is_adjacent(14, 15)
        assert b.is_adjacent(1, 1)
        assert b.is_adjacent(5, 10)
        assert b.is_adjacent(1, 4)

    def test_five_by_three(self):
        b = boggle(5, 3)
        assert b.is_adjacent(0, 1)
        assert b.is_adjacent(6, 7)
        assert b.is_adjacent(12, 13)
        assert b.is_adjacent(0, 7) is False
        assert b.is_adjacent(3, 13) is False
        assert b.is_adjacent(0, 14) is False
        assert b.is_adjacent(1, 7)
        assert b.is_adjacent(9, 13)
        assert b.is_adjacent(4, 8)

    def test_get_adjacent53(self):
        b = boggle(5, 3)
        # middle
        adj = b.get_adjacent(6)
        t = [0, 1, 2, 5, 7, 10, 11, 12]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # middle - except some already visited
        adj = b.get_adjacent(6, [0, 1, 7, 11])
        t = [2, 5, 10, 12]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side
        adj = b.get_adjacent(9)
        t = [3, 4, 8, 13, 14]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side - except some already visited
        adj = b.get_adjacent(9, [4, 13, 1])
        t = [3, 8, 14]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner
        adj = b.get_adjacent(0)
        t = [1, 5, 6]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner - except some already visited
        adj = b.get_adjacent(0, [5, 4, 9])
        t = [1, 6]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

    def test_get_adjacent44(self):
        b = boggle(4, 4)

        # middle
        adj = b.get_adjacent(6)
        t = [1, 2, 3, 5, 7, 9, 10, 11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # middle - except some already visited
        adj = b.get_adjacent(6, [2, 4, 6, 10])
        t = [1, 3, 5, 7, 9, 11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side
        adj = b.get_adjacent(7)
        t = [2, 3, 6, 10, 11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # side - except some already visited
        adj = b.get_adjacent(7, [3, 10, 20, 500])
        t = [2, 6, 11]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner
        adj = b.get_adjacent(12)
        t = [8, 9, 13]
        for index in t:
            assert index in adj
        assert len(adj) is len(t)

        # corner - except some already visited
        adj = b.get_adjacent(12, [8, 9, 13])
        assert len(adj) is 0


class test_dictionary(unittest.TestCase):

    """Unit tests for the dictionary."""

    def test_hi(self):
        ed = e_dict()
        ed.add_word("hi")
        assert(ed.is_word("hi"))

    def test_casesensetive(self):
        ed = e_dict()
        ed.add_word("ThEoDoRe")
        assert(ed.is_word("theodore"))
        assert(ed.is_word("THEODORE"))
        assert(ed.is_word("THEOdore"))

    def test_multiplewordswithsameroot(self):
        ed = e_dict()
        ed.add_word("he")
        ed.add_word("HELL")
        ed.add_word("HELLo")
        assert(ed.is_word("he"))
        assert(ed.is_word("hell"))
        assert(ed.is_word("hello"))
        assert(False is ed.is_word("h"))
        assert(False is ed.is_word("hel"))

    def test_read_dict_bad_path(self):
        ed = e_dict()
        bad_path = "obviosly_bad_FILE-pAtH_god_i?hopethsIsnot_an_actualpath.garbled"
        try:
            ed.read_dictionary(bad_path)
        except OSError as err:
            assert err.errno == 2
            assert err.filename == bad_path
            assert err.strerror == 'No such file or direcotory'

    def test_is_still_valid(self):
        ed = e_dict()
        ed.read_dictionary(True)
        assert ed.is_still_potentially_valid("ortho")
        assert ed.is_still_potentially_valid("orthorhombic")
        assert ed.is_still_potentially_valid("orthorhombics") is False
        assert ed.is_still_potentially_valid("1") is False
        assert ed.is_still_potentially_valid("aa")
        assert ed.is_still_potentially_valid("A")
        assert ed.is_still_potentially_valid("AaA") is False

    def test_get_words(self):
        ed = e_dict()
        ed.read_dictionary(True)
        words = ed.get_words(ed.dictionary_root)
        print(words)
        dict_words = test_word_list
        for word in dict_words:
            print(word)
            assert word.lower() in words
        assert len(words) is len(dict_words)

if __name__ == '__main__':
    unittest.main()
