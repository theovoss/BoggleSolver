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

f_name = os.path.join("..", "..", "docs", "twl06.txt")
test_name = os.path.join("..", "..", "docs", "test_words.txt")


class test_everything(unittest.TestCase):

    """
    All integration Tests.

    These tests all take a somewhat significant amount of time, usually due to loading in the dictionary.
    Could speed these up a lot if I store that dictionary globally.
    """

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

    def test_search_speed_vs_raw_read(self):
        d = e_dict()
        d.read_dictionary(f_name)

        t = open(test_name)
        test_words = t.readlines()
        t.close()

        f = open(f_name)
        p = open(f_name)
        allwords = f.read()
        alllines = p.readlines()
        f.close()
        p.close()

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

    def test_loads_all_words(self):
        d = e_dict()
        d.read_dictionary(f_name)

        f = open(f_name)

        for line in f.readlines():
            d.is_word(line.lower().strip())
            assert d.is_word(line.lower().strip())

        f.close()

    def test_against_my_sql(self):
        d = e_dict()
        d.read_dictionary(f_name)

        f = open(f_name)

        num_slower_than_sql = 0

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE my_dict (word text)''')

        for word in f.readlines():
            c.execute("INSERT INTO my_dict VALUES (?)", [word])

        f.close()

        conn.commit()

        t = open(test_name)
        test_words = t.readlines()
        t.close()

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
