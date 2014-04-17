import unittest
import os.path
import sys
sys.path.insert(0,'..\\')
from load_english_dictionary import e_dict

class test_add_word(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
