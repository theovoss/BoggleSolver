#!/usr/bin/env python

"""Class to solve the boggle boggle_board."""


from bogglesolver.boggle_board import Boggle
from bogglesolver.load_english_dictionary import e_dict


class solve_boggle:

    """
    Class to solve a boggle board.

    This initializes the dictionary and board.
    Then it searches the board for all valid words.
    """

    def __init__(self, boggle_array, columns, rows, use_test_words=False):
        self.use_test_words = use_test_words
        self.e_dict = e_dict()
        self.e_dict.read_dictionary(self.use_test_words)
        self.boggle = Boggle(columns, rows)
        self.boggle.set_array(boggle_array)

    def solve(self, normal_adj=True):
        words = []
        for i, letter in enumerate(self.boggle.boggle_array):
            w = self.recurse_search_for_words(i, letter, '', None, normal_adj=normal_adj)
            words += w
        return sorted(set(words))

    def recurse_search_for_words(self, a_index, letter, word, indexes_searched=None, normal_adj=True):
        if indexes_searched is None:
            indexes_searched = []
        retVal = []
        for index in self.boggle.get_adjacent(a_index, indexes_searched, normal_adj=normal_adj):
            searched = indexes_searched + [index]
            # need to read more into parameter scope in recursion: http://stackoverflow.com/questions/14084666/python-recursive-function-variable-scope
            if self.e_dict.is_still_potentially_valid(word + letter):
                retVal += self.recurse_search_for_words(index, self.boggle.boggle_array[index], word + letter, searched, normal_adj=normal_adj)
        if self.e_dict.is_word(word + letter) and (word + letter) not in retVal:
            retVal.append(word + letter)
        return retVal
