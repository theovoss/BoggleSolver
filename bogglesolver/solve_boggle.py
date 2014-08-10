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

    def __init__(self, use_test_words=False):
        self.use_test_words = use_test_words
        self.edict = Edict()
        self.edict.read_dictionary(self.use_test_words)
        self.boggle = Boggle()
        self.min_word_len = 3

    def set_board(self, columns, rows, boggle_list=None):
        """
        Set the board for the game.

        :param int columns: number of columns for the board.
        :param int rows: number of rows for the board.
        :param boggle_list: list of all the letters for the board (optional).
        :type boggle_list: list or None
        """
        self.boggle.num_columns = columns
        self.boggle.num_rows = rows
        self.boggle.size = columns * rows
        print("Size is: %s, columns are: %s, rows are: %s" % (self.boggle.size, self.boggle.num_columns, self.boggle.num_rows))
        if boggle_list is not None:
            self.boggle.set_array(boggle_list)
        else:
            self.boggle.generate_boggle_board()

    def solve(self, ignore_indexes=None, normal_adj=True):
        """
        Solve the boggle board, or get all words for scrabble.

        :param bool normal_adj: True to solve for boggle.
                                False to solve for scrabble.
        :returns: sorted list of all words found.
        """
        if ignore_indexes is None:
            ignore_indexes = []
        assert self.boggle.is_full(), "Boggle board has not been set."
        node = self.edict.dictionary_root
        words = []
        keys = node.letters.keys()
        for i, letter in enumerate(self.boggle.boggle_array):
            if i not in ignore_indexes and letter in keys:
                self.recurse_search_for_words(i, letter, '', node,
                                              ignore_indexes + [i], normal_adj, words)
        return sorted(set(words))

    def recurse_search_for_words(self, a_index, letter, word, node,
                                 indexes_searched, normal_adj, words=[]):
        """
        Recursively search boggle board for words.

        :param int a_index: index in the word.
        :param str letter: current letter.
        :param str word: current potential word.
        :param indexes_searched: indexes searched already.
        :type indexes_searched: None or list.
        :param bool normal_adj: whether to solve for boggle or scrabble.
        """
        new_word = word + letter
        new_node = node.letters[letter]
        keys = new_node.letters.keys()
        if new_node.is_word and (len(new_word) >= self.min_word_len):
            words.append(new_word)
        adj = self.boggle.get_adjacent(a_index, indexes_searched, normal_adj)
        for index in adj:
            if self.boggle.boggle_array[index] in keys:
                self.recurse_search_for_words(index, self.boggle.boggle_array[index],
                                              new_word, new_node, indexes_searched + [index],
                                              normal_adj, words)
