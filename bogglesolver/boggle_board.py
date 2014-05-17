#!/usr/bin/env python

"""Classes that keep track of the board."""


class boggle:

    """
    The boggle board.

    This represents the physical board and where each letter is.
    """

    def __init__(self, num_columns=5, num_rows=5):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.boggle_array = [None] * (self.num_columns * self.num_rows)
        self.size = self.num_columns * self.num_rows

    def is_adjacent(self, index_1, index_2):
        retVal = False

        row_1 = index_1 // self.num_columns
        row_2 = index_2 // self.num_columns
        column_1 = index_1 % self.num_columns
        column_2 = index_2 % self.num_columns

        rows_are_less_than_1_away = abs(row_2 - row_1) <= 1
        columns_are_less_than_1_away = abs(column_2 - column_1) <= 1
        if rows_are_less_than_1_away and columns_are_less_than_1_away:
            retVal = True

        return retVal

    def get_adjacent(self, index, ignore=None):
        if ignore is None:
            ignore = []
        retVal = []
        for i in range(0, self.num_columns * self.num_rows):
            if self.is_adjacent(index, i) and (i is not index) and (i not in ignore):
                retVal.append(i)
        return retVal

    def insert(self, character, index):
        if index < len(self.boggle_array):
            self.boggle_array[index] = character

    def is_full(self):
        for i in range(0, self.size):
            if self.boggle_array[i] is None:
                return False
        return True

    def set_array(self, array):
        self.boggle_array = array