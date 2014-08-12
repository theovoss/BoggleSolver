#!/usr/bin/env python

"""Integration tests for all boggle classes."""


import sys
import unittest
import os.path
import time
import sqlite3
import os

import boggleboard

from bogglesolver.load_english_dictionary import Edict
from bogglesolver.boggle_board import Boggle
from bogglesolver.solve_boggle import SolveBoggle

from bogglesolver.twl06 import WORD_LIST
from bogglesolver.twl06 import TEST_WORD_LIST


class test_solve_boggle(unittest.TestCase):

    """Unit tests for the solve boggle class."""

    # @unittest.skip("Skipping solve tests.")
    def test_init(self):
        """Test solve boggle."""
        columns = 5
        rows = 1
        array = ["w", "a", "t", "e", "r"]
        solve_game = SolveBoggle(True)
        solve_game.set_board(columns, rows, array)
        solve_game.edict.add_word("wata")
        solve_game.edict.add_word("wate")
        solve_game.edict.add_word("a")
        solve_game.edict.add_word("tear")
        solve_game.edict.add_word("tea")
        solve_game.edict.add_word("eat")
        solved = solve_game.solve()
        assert "water" in solved
        assert "a" not in solved
        assert "wata" not in solved
        assert "wate" in solved
        assert "eat" not in solved
        assert "tear" not in solved
        assert "tea" not in solved

        solve_game.min_word_len = 0
        solved = solve_game.solve()
        assert "a" in solved

        solved = solve_game.solve(normal_adj=False)
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

    # @unittest.skip("Skipping integration tests.")
    def test_solves_Boggle(self):
        """Test solving the boggle board."""
        columns = 4
        rows = 4
        array = "a b c d e f g h i j k l m n o p".split()

        assert len(array) == columns * rows

        solve_game = SolveBoggle()
        solve_game.set_board(columns, rows, array)

        # found words from: http://www.bogglecheat.net/, though may not be in my dictionary
        known_words = ["knife", "mino", "bein", "fink", "nife", "glop", "polk", "mink", "fino", "jink", "nief", "knop", "ink", "fin", "jin", "nim", "kop", "pol", "fab", "fie", "nie", "kon", "lop", "ab", "ef", "if", "mi", "be", "jo", "ch", "on", "lo", "ae", "ea", "in", "ba", "fa", "no", "ko", "op", "po"]
        for word in known_words:
            solve_game.edict.add_word(word)

        solve_game.min_word_len = 5
        solved = solve_game.solve()

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

        solve_game.min_word_len = 0
        solved = solve_game.solve()

        for word in known_words:
            if len(word) >= solve_game.min_word_len:
                assert word in solved
            else:
                assert word not in solved

    # @unittest.skip("Skipping integration tests.")
    def test_search_speed_vs_raw_read(self):
        """Test search speed."""
        my_dict = Edict()
        my_dict.read_dictionary()

        test_words = TEST_WORD_LIST

        allwords = ' '.join(WORD_LIST)
        alllines = WORD_LIST

        num_slower_than_read = 0
        num_slower_than_readlines = 0

        time1 = time.time()
        time2 = time.time()

        for a_word in test_words:
            word = a_word
            lower = a_word.lower().strip()
            if not my_dict.is_word(lower):
                print(word)

            time1 = time.time()
            assert my_dict.is_word(lower)
            time2 = time.time()
            dict_time = time2 - time1

            time1 = time.time()
            if word not in allwords:
                assert False
            time2 = time.time()
            all_time = time2 - time1

            time1 = time.time()
            if word not in alllines:
                assert False
            time2 = time.time()
            line_time = time2 - time1

            if dict_time > all_time:
                # print (word)
                num_slower_than_read += 1
            if dict_time > line_time:
                # print (word)
                num_slower_than_readlines += 1

        assert num_slower_than_read <= 1
        assert num_slower_than_readlines <= 1

    # @unittest.skip("Skipping integration tests.")
    def test_loads_all_words(self):
        """Test the dictionary can load all the words."""
        my_dict = Edict()
        my_dict.read_dictionary()

        for line in WORD_LIST:
            my_dict.is_word(line.lower())
            assert my_dict.is_word(line.lower())

    # @unittest.skip("Skipping integration tests.")
    def test_against_my_sql(self):
        """Test searching in custom dictionary is faster than in my_sql."""
        my_dict = Edict()
        my_dict.read_dictionary()

        num_slower_than_sql = 0

        conn = sqlite3.connect('example.db')
        con = conn.cursor()
        con.execute('''CREATE TABLE my_dict (word text)''')

        for word in WORD_LIST:
            con.execute("INSERT INTO my_dict VALUES (?)", [word])

        conn.commit()

        test_words = TEST_WORD_LIST

        time1 = time.time()
        time2 = time.time()
        for word in test_words:
            time1 = time.time()
            my_dict.is_word(word)
            time2 = time.time()
            d_time = time2 - time1

            time1 = time.time()
            con.execute('SELECT * FROM my_dict WHERE word=?', [word])
            time2 = time.time()
            b_time = time2 - time1

            if d_time > b_time:
                num_slower_than_sql += 1
                print("D time is: " + str(d_time))
                print("B time is: " + str(b_time))
        con.close()
        conn.close()

        os.remove("example.db")

        assert num_slower_than_sql <= 1


# @unittest.skipUnless(os.getenv(ENV), REASON)
class test_speed_against_other_libraries(unittest.TestCase):

    """Test my boggle library against other boggle libraries."""

    def test_pypi_init_speeds(self):
        """Test how fast they load."""
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e', 'r', 'i', 'u', 'c', 't', 's', 'i', 'e', 'a', 'n', 'i', 'a']

        t1 = time.time()
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)
        t2 = time.time()

        my_time = t2 - t1

        print("My init time is: %s" % my_time)
        assert my_time < 4

    def test_pypi_4_by_4(self):
        """Test 4x4 against the current boggle board on pypi."""
        other_default_size = 4
        letters = ['i', 'r', 'e', 'e',
                   'r', 'i', 'u', 'c',
                   't', 's', 'i', 'e',
                   'a', 'n', 'i', 'a']

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()

        my_solve_time = t2 - t1

        print("I found %s words in %s time." % (my_solve_time, len(my_words)))

        assert len(my_words) == 77
        assert my_solve_time < 0.01

    def test_pypi_10_by_10(self):
        """Test 10x10 against the current boggle board on pypi."""
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

        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size, letters)

        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()

        my_solve_time = t2 - t1

        print("I took %s seconds to find %s words." % (my_solve_time, len(my_words)))
        assert len(my_words) == 1973
        assert my_solve_time < 0.11

    def test_100x100_time(self):
        """Test 100x100 against the current boggle board on pypi."""
        other_default_size = 100
        my_boggle = SolveBoggle()
        my_boggle.set_board(other_default_size, other_default_size)

        t1 = time.time()
        my_words = my_boggle.solve()
        t2 = time.time()

        my_solve_time = t2 - t1

        print("Found %s words." % len(my_words))
        print("Took %s seconds to solve 100x100." % my_solve_time)

        # make sure we can solve 100x100 in a reasonable ammount of time.
        assert my_solve_time < 20


if __name__ == '__main__':
    unittest.main()
