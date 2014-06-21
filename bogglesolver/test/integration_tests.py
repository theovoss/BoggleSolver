#!/usr/bin/env python

"""Integration tests for all boggle classes."""


import sys
import unittest
import os.path
import time
import sqlite3
import os

from bogglesolver.load_english_dictionary import e_dict
from bogglesolver.boggle_board import boggle
from bogglesolver.solve_boggle import solve_boggle

from bogglesolver.twl06 import word_list
from bogglesolver.twl06 import test_word_list


class test_solve_boggle(unittest.TestCase):

    """Unit tests for the solve boggle class."""

    # @unittest.skip("Skipping solve tests.")
    def test_init(self):
        self.columns = 5
        self.rows = 1
        array = ["w", "a", "t", "e", "r"]
        sb = solve_boggle(array, self.columns, self.rows, True)
        sb.e_dict.add_word("wata")
        sb.e_dict.add_word("wate")
        sb.e_dict.add_word("a")
        sb.e_dict.add_word("tear")
        sb.e_dict.add_word("tea")
        sb.e_dict.add_word("eat")
        solved = sb.solve()
        assert "water" in solved
        assert "a" in solved
        assert "wata" not in solved
        assert "wate" in solved
        assert "eat" not in solved
        assert "tear" not in solved
        assert "tea" not in solved

        solved = sb.solve(False)
        print(solved)
        assert "water" in solved
        assert "a" in solved
        assert "wata" not in solved
        assert "wate" in solved
        assert "eat" in solved
        assert "tea" in solved
        assert "tear" in solved


class test_everything(unittest.TestCase):

    """
    All integration Tests.

    These tests all take a somewhat significant amount of time, usually due to loading in the dictionary.
    Could speed these up a lot if I store that dictionary globally.
    """

    def test_generate_board(self):
        b = boggle(4, 4)
        b.generate_boggle_board()
        assert b.is_full()

    # @unittest.skip("Skipping integration tests.")
    def test_solves_boggle(self):
        self.columns = 4
        self.rows = 4
        array = "a b c d e f g h i j k l m n o p".split()

        sb = solve_boggle(array, self.columns, self.rows)

        # found words from: http://www.bogglecheat.net/, though may not be in my dictionary
        known_words = ["knife", "mino", "bein", "fink", "nife", "glop", "polk", "mink", "fino", "jink", "nief", "knop", "ink", "fin", "jin", "nim", "kop", "pol", "fab", "fie", "nie", "kon", "lop", "ab", "ef", "if", "mi", "be", "jo", "ch", "on", "lo", "ae", "ea", "in", "ba", "fa", "no", "ko", "op", "po"]
        for word in known_words:
            sb.e_dict.add_word(word)

        solved = sb.solve()

        for word in known_words:
            if word not in solved:
                print(word)
                assert False

    # @unittest.skip("Skipping integration tests.")
    def test_search_speed_vs_raw_read(self):
        d = e_dict()
        d.read_dictionary()

        test_words = test_word_list

        allwords = ' '.join(word_list)
        alllines = word_list

        num_slower_than_read = 0
        num_slower_than_readlines = 0

        t1 = time.time()
        t2 = time.time()

        for a_word in test_words:
            word = a_word
            lower = a_word.lower().strip()
            if not d.is_word(lower):
                print(word)

            t1 = time.time()
            assert d.is_word(lower)
            t2 = time.time()
            dict_time = t2 - t1

            t1 = time.time()
            if word not in allwords:
                assert False
            t2 = time.time()
            all_time = t2 - t1

            t1 = time.time()
            if word not in alllines:
                assert False
            t2 = time.time()
            line_time = t2 - t1

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
        d = e_dict()
        d.read_dictionary()

        for line in word_list:
            d.is_word(line.lower())
            assert d.is_word(line.lower())

    # @unittest.skip("Skipping integration tests.")
    def test_against_my_sql(self):
        d = e_dict()
        d.read_dictionary()

        num_slower_than_sql = 0

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE my_dict (word text)''')

        for word in word_list:
            c.execute("INSERT INTO my_dict VALUES (?)", [word])

        conn.commit()

        test_words = test_word_list

        t1 = time.time()
        t2 = time.time()
        for word in test_words:
            t1 = time.time()
            d.is_word(word)
            t2 = time.time()
            d_time = t2 - t1

            t1 = time.time()
            c.execute('SELECT * FROM my_dict WHERE word=?', [word])
            t2 = time.time()
            b_time = t2 - t1

            if d_time > b_time:
                num_slower_than_sql += 1
                print("D time is: " + str(d_time))
                print("B time is: " + str(b_time))
        c.close()
        conn.close()

        os.remove("example.db")

        assert num_slower_than_sql <= 1

if __name__ == '__main__':
    unittest.main()
