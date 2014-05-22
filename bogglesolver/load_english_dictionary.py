#!/usr/bin/env python

"""Stores the dictionary in a linked list."""


import os.path


class dict_node:

    """
    An element of the dictionary.

    Each element represents one letter in a word.
    Each element contains an array of potential next elements.
    This means that look-up time for a word depends only on the length of the word.
    It also means that if you have a partial word, all potential endings are further down the tree.
    """

    def __init__(self):
        self.is_word = False
        self.letters = {}
        self.word = ""

    def add_letter(self, word, index):
        if len(word) > index:  # if we have index+1 here, we start getting results in is_word for solve boggle tests.
            if word[index] in self.letters.keys():
                self.letters[word[index]].add_letter(word, index + 1)
            else:
                self.letters[word[index]] = dict_node()
                self.letters[word[index]].add_letter(word, index + 1)
        else:
            self.is_word = True
            self.word = word


class e_dict:

    """
    The interface for the dictionary.

    Contains the root element of the dictionary.
    Contains helpful functions for creating, adding to, and accessing the dictionary elements.
    """

    def __init__(self):
        self.dictionary_root = dict_node()

    def read_dictionary(self, filepath):
        if os.path.exists(filepath):
            f = open(filepath)
            lines = f.readlines()
            for line in lines:
                self.add_word(line.lower().strip())
            f.close()
        else:
            print(filepath)
            print(os.path.abspath(filepath))
            raise OSError(2, 'No such file or direcotory', str(filepath))

    def is_word(self, word):
        retVal = False
        node = self.get_node(word)
        if node is not None:
            retVal = node.is_word
        return retVal

    def add_word(self, word):
        self.dictionary_root.add_letter(word.lower(), 0)

    def get_words(self, node, values=[]):
        for n in node.letters.keys():
            values = self.get_words(node.letters[n], values)
        if node.is_word and node.word not in values:
            values.append(node.word)
        return values

    def get_node(self, string):
        word = string.lower()
        node = self.dictionary_root
        for i in range(0, len(word)):
            if word[i] in node.letters.keys():
                node = node.letters[word[i]]
            else:
                node = None
                break
        return node

    def is_still_potentially_valid(self, word):
        node = self.get_node(word)
        return node is not None
