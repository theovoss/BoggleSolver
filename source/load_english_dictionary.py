import os.path

class dict_node:
    def __init__(self):
        self.is_word = False
        self.current = None
        self.next_letter = None
        self.letters = {}
        self.is_word = False

    def add_letter (self, word, index):
        if len(word) > index:
            if word[index] in self.letters.keys():
                self.letters[word[index]].add_letter(word, index+1)
            else:
                self.letters[word[index]] = dict_node()
                self.letters[word[index]].add_letter(word, index+1)
        else:
            self.is_word = True


class e_dict:
    def __init__(self):
        self.dictionary_root = dict_node()

    def read_dictionary (self,filepath):
        if os.path.exists(filepath):
            f = open(filepath)
            lines = f.readlines()
            for line in lines:
                self.add_word(line.lower())
        else:
            print (filepath)
            print (os.path.abspath(filepath))
            assert False

    def is_word(self,a_word):
        word = a_word.lower()
        node = self.dictionary_root
        for i in range(0,len(word)):
            if word[i] in node.letters.keys():
                node = node.letters[word[i]]
        return node.is_word

    def add_word (self, word):
        self.dictionary_root.add_letter(word.lower(),0)

    def print_words():
        for i in self.dictionary_root.keys():
            j = 0


