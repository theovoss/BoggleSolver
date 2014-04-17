import sys
import unittest
import os.path
import time

sys.path.insert(0,'..\\')
from load_english_dictionary import e_dict

f_name = "..\\..\\docs\\english_words.txt"
test_name = "..\\..\\docs\\test_words.txt"

class test_everything(unittest.TestCase):
    def test_search_speed_vs_raw_read(self):
        d = e_dict()
        d.read_dictionary(f_name)

        t = open(test_name)
        test_words = t.readlines()

        f = open(f_name)
        p = open(f_name)
        allwords = f.read()
        alllines = p.readlines()

        t1 = time.time()
        t2 = time.time()
        for a_word in test_words:
            word = a_word
            lower = a_word.lower()
            
            t1 = time.time()
            assert d.is_word(lower)
            t2 = time.time()
            dict_time = t2-t1

            t1 = time.time()
            if word not in allwords:
                assert False
            t2 = time.time()
            all_time = t2-t1

            t1 = time.time()
            if word not in alllines:
                assert False
            t2 = time.time()
            line_time = t2-t1

            assert dict_time <= all_time
            assert dict_time <= line_time

    def test_loads_all_words(self):
        d = e_dict()
        d.read_dictionary(f_name)

        f = open(f_name)

        for line in f.readlines():
            d.is_word(line.lower())
            assert d.is_word(line.lower())



if __name__ == '__main__':
    unittest.main()
