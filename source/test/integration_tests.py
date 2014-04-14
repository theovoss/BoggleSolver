import sys
import unittest

sys.path.insert(0,'..\\')
import load_english_dictionary

f_name = "../docs/english_words.txt"

d = dictionary()
d.read_dictionary(f_name)

f = open(f_name)

print ("Done reading")

for line in f.readlines():
    d.is_word(line.lower())
    assert d.is_word(line.lower())
