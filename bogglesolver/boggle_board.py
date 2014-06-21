#!/usr/bin/env python

"""Classes that keep track of the board."""


from bogglesolver.twl06 import word_list
import random


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

    def __str__(self):
        string = ""
        if self.is_full():
            print(self.boggle_array)
            for i, letter in enumerate(self.boggle_array):
                print(letter)
                if (i % self.num_columns is 0) and (i is not 0):
                    string += " |\n"
                string += " | " + letter
        
            string += " |\n"
        return string

    def generate_boggle_board(self):
        combined_words = ''.join(word_list)
        array = []
        for i in range(0, self.size):
            r = random.randint(0, len(combined_words) - 1)
            array.append(combined_words[r])
        self.boggle_array = array

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

    def get_adjacent(self, index, ignore=None, normal_adj=True):
        print("Normal_adj is: %s" % normal_adj)
        if ignore is None:
            ignore = []
        retVal = []
        for i in range(0, self.num_columns * self.num_rows):
            if (not normal_adj or self.is_adjacent(index, i)) and \
               (i is not index) and (i not in ignore):
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
