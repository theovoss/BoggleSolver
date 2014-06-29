#!/usr/bin/env python

"""Classes that keep track of the board."""


from bogglesolver.twl06 import WORD_LIST
import random


class Boggle:

    """
    The boggle board.

    This represents the physical board and where each letter is.
    """

    def __init__(self, num_columns=5, num_rows=5):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.boggle_array = [None] * (self.num_columns * self.num_rows)
        self.size = self.num_columns * self.num_rows

    def __str__(self):
        string = ""
        if self.is_full():
            for i, letter in enumerate(self.boggle_array):
                if (i % self.num_columns is 0) and (i is not 0):
                    string += " |\n"
                string += " | " + letter

            string += " |\n"
        return string

    def generate_boggle_board(self):
        """Generate a boggle board by randomly selecting letters from valid words."""
        combined_words = ''.join(WORD_LIST)
        array = []
        for i in range(0, self.size):
            random_number = random.randint(0, len(combined_words) - 1)
            self.boggle_array[i] = combined_words[random_number]

    def is_adjacent(self, index_1, index_2):
        """
        Determine if two indexes are adjacent.

        :param int index_1: first index
        :param int index_2: second index
        :returns: True if the indexes are adjacent. False otherwise.
        """
        ret_val = False

        row_1 = index_1 // self.num_columns
        row_2 = index_2 // self.num_columns
        column_1 = index_1 % self.num_columns
        column_2 = index_2 % self.num_columns

        rows_are_less_than_1_away = abs(row_2 - row_1) <= 1
        columns_are_less_than_1_away = abs(column_2 - column_1) <= 1
        if rows_are_less_than_1_away and columns_are_less_than_1_away:
            ret_val = True

        return ret_val

    def get_adjacent(self, index, ignore=None, normal_adj=True):
        """
        Get all adjacent indexes.

        Ignore is meant to be the disabled or previously traversed indexes.
        Normal_adj is to toggle between finding words in a boggle board
            and finding all possible words for scrabble.
            True is find words in boggle board. False is to find scrabble
            words.

        :param int index: index to get all adjacent indexes of.
        :param list ignore: optional list of indexes to ignore.
        :param bool normal_adj: whether to use the normal is adjacent
               or ignore it.
        :returns: True if adjacent. False otherwise.
        """
        if ignore is None:
            ignore = []
        ret_val = []
        for i in range(0, self.num_columns * self.num_rows):
            if (not normal_adj or self.is_adjacent(index, i)) and \
               (i is not index) and (i not in ignore):
                ret_val.append(i)
        return ret_val

    def insert(self, character, index):
        """
        Insert a character into the boggle array.

        :param str character: character to insert.
        :param int index: index to insert the character at.
        """
        if index < len(self.boggle_array):
            self.boggle_array[index] = character

    def is_full(self):
        """
        If the boggle board has been completely filled.

        :returns: True if full. False otherwise.
        """
        for i in range(0, self.size):
            if self.boggle_array[i] is None:
                return False
        return True

    def set_array(self, array):
        """
        Set the boggle array with the one provided.

        :param list array: list to set the boggle array to.
        """
        self.boggle_array = array
