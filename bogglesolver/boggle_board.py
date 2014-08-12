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
        self.boggle_array = []
        for i in range(0, self.num_columns * self.num_rows):
            random_number = random.randint(0, len(combined_words) - 1)
            self.boggle_array.append(combined_words[random_number])

    def get_adjacent(self, index, ignore=None, normal_adj=True, keys=None):
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
        if keys is None:
            keys = []

        # if not normal adjacent
        if normal_adj:
            row = index // self.num_columns
            column = index % self.num_columns

            # calculate the 8 indexes that surround this index

            # index directly to the left:
            if column != 0:
                one_less = index - 1
                if one_less not in ignore:
                    if self.boggle_array[one_less] in keys:
                        yield one_less
                # diagonal up and left
                if row != 0 and one_less - self.num_columns not in ignore:
                    if self.boggle_array[one_less - self.num_columns] in keys:
                        yield one_less - self.num_columns
                # diagonal down and left
                if row != self.num_rows - 1 and one_less + self.num_columns not in ignore:
                    if self.boggle_array[one_less + self.num_columns] in keys:
                        yield one_less + self.num_columns

            # index directly to the right:
            if column != self.num_columns - 1:
                one_more = index + 1
                if one_more not in ignore:
                    if self.boggle_array[one_more] in keys:
                        yield one_more
                # index to the top right
                if row != 0 and one_more - self.num_columns not in ignore:
                    if self.boggle_array[one_more - self.num_columns] in keys:
                        yield one_more - self.num_columns
                # index to the bottom right
                if row != self.num_rows - 1 and one_more + self.num_columns not in ignore:
                    if self.boggle_array[one_more + self.num_columns] in keys:
                        yield one_more + self.num_columns

            # directly above
            if row != 0 and index - self.num_columns not in ignore:
                if self.boggle_array[index - self.num_columns] in keys:
                    yield index - self.num_columns

            # directly below
            if row != self.num_rows - 1 and index + self.num_columns not in ignore:
                if self.boggle_array[index + self.num_columns] in keys:
                    yield index + self.num_columns

        else:
            for i in range(0, self.num_rows * self.num_columns):
                if i not in ignore and i is not index and self.boggle_array[i] in keys:
                    yield i

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
        ret_val = True
        size = self.num_rows * self.num_columns
        if len(self.boggle_array) == size:
            for i in range(0, size):
                if self.boggle_array[i] is None:
                    ret_val = False
                    print("Found element of array that was None.")
        else:
            print("Boggle array len: %s does not equal size: %s." % (len(self.boggle_array), size))
            ret_val = False
        return ret_val

    def set_array(self, array):
        """
        Set the boggle array with the one provided.

        :param list array: list to set the boggle array to.
        """
        self.boggle_array = array
