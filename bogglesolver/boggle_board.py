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
        for _ in range(0, self.num_columns * self.num_rows):
            random_number = random.randint(0, len(combined_words) - 1)
            self.boggle_array.append(combined_words[random_number])

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
