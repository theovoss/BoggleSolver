import os.path

class dict_node:
    def __init__(self):
        self.is_word = False
        self.letters = {}
        self.word = ""

    def add_letter (self, word, index):
        if len(word) > index: # if we have index+1 here, we start getting results in is_word for solve boggle tests.
            if word[index] in self.letters.keys():
                self.letters[word[index]].add_letter(word, index+1)
            else:
                self.letters[word[index]] = dict_node()
                self.letters[word[index]].add_letter(word, index+1)
        else:
            self.is_word = True
            self.word = word
            print ("Depth is: " + str(index) + " for word " + word)
            


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
        f.close()

    def is_word(self,word):
        retVal = False
        node = self.get_node(word)
        if node is not None:
            retVal = node.is_word
        return retVal

    def add_word (self, word):
        self.dictionary_root.add_letter(word.lower(),0)
        print ("word added: " + word)

    def get_words(self,node):
        for i in node.letters:
            if i is not None:
                self.get_words(node)
        print (node.letters)
        return
    
    def get_node(self,string):
        word = string.lower()
        node = self.dictionary_root
        for i in range(0,len(word)):
            if word[i] in node.letters.keys():
                node = node.letters[word[i]]
            else:
                node = None
        return node

    def is_still_potentially_valid(self,word):
        node = self.get_node(word)
        return node is not None



