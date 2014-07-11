#!/usr/bin/env python

"""Class to solve the boggle boggle_board."""


from bogglesolver.boggle_board import Boggle
from bogglesolver.load_english_dictionary import Edict


class SolveBoggle:

    """
    Class to solve a boggle board.

    This initializes the dictionary and board.
    Then it searches the board for all valid words.
    """

    def __init__(self, boggle_array, columns, rows, use_test_words=False):
        self.use_test_words = use_test_words
        self.edict = Edict()
        self.edict.read_dictionary(self.use_test_words)
        self.boggle = Boggle(columns, rows)
        if boggle_array:
            self.boggle.set_array(boggle_array)
        else:
            self.boggle.generate_boggle_board()

    def solve(self, ignore_indexes=None, normal_adj=True):
        """
        Solve the boggle board, or get all words for scrabble.

        :param bool normal_adj: True to solve for boggle.
                                False to solve for scrabble.
        :returns: sorted list of all words found.
        """
        words = []
        for i, letter in enumerate(self.boggle.boggle_array):
            words += self.recurse_search_for_words(i, letter, '', self.edict.dictionary_root,
                                                   indexes_searched=ignore_indexes,
                                                   normal_adj=normal_adj)
        return sorted(set(words))

    def recurse_search_for_words(self, a_index, letter, word, node,
                                 indexes_searched=None, normal_adj=True):
        """
        Recursively search boggle board for words.

        TODO: shouldn't need letter.

        :param int a_index: index in the word.
        :param str letter: current letter.
        :param str word: current potential word.
        :param indexes_searched: indexes searched already.
        :type indexes_searched: None or list.
        :param bool normal_adj: whether to solve for boggle or scrabble.
        """
        if indexes_searched is None:
            indexes_searched = []
        ret_val = []
        for index in self.boggle.get_adjacent(a_index, indexes_searched,
                                              normal_adj=normal_adj):
            searched = indexes_searched + [index]
            if self.edict.is_valid_path(node, letter):
                ret_val += self.recurse_search_for_words(index, self.boggle.boggle_array[index], word + letter, node.letters[letter], indexes_searched=searched, normal_adj=normal_adj)
        if self.edict.is_word(word + letter) and (word + letter) not in ret_val:
            ret_val.append(word + letter)
        return ret_val
