import sys
import unittest
import os.path

sys.path.insert(0,'..\\')
from load_english_dictionary import dictionary as e_dict

f_name = "..\\..\\docs\\english_words.txt"

d = e_dict()
d.read_dictionary(f_name)

f = open(f_name)

print ("Done reading")

for line in f.readlines():
    d.is_word(line.lower())
    assert d.is_word(line.lower())

print ("found all words")


