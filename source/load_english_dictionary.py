
class dict_node:
    def __init__(self):
        self.is_word = False
        self.current = None
        self.next_letter = None
        self.letters = {}
        self.is_word = False

    def add_word (self, word):
        #self.current = word[0]
        self.add_letter(word,0)

    def add_letter (self, word, index):
        if len(word) > index:
            # self.current = word[index]
            if word[index] in self.letters.keys():
                self.letters[word[index]].add_letter(word, index+1)
            else:
                self.letters[word[index]] = dict_node()
                self.letters[word[index]].add_letter(word, index+1)
        else:
            self.is_word = True
            # print ("Just added word: " + word + " current index: " + str(index))


class dictionary:
    def __init__(self):
        self.dictionary_root = dict_node()
    def read_dictionary (self,filepath):
        f = open(filepath)
        lines = f.readlines()
        for line in lines:
            self.dictionary_root.add_word(line.lower())
        print (self.dictionary_root)

    def is_word(self,word):
        node = self.dictionary_root
        for i in range(0,len(word)):
            if node.is_word:
                print (word[0:i] + " is a word")
            if word[i] in node.letters.keys():
                node = node.letters[word[i]]
        return node.is_word

    def print_words():
        for i in self.dictionary_root.keys():
            j = 0

f_name = "..\docs\english_words.txt"

d = dictionary()
d.read_dictionary(f_name)

f = open(f_name)

print ("Done reading")

for line in f.readlines():
    d.is_word(line.lower())
    if not d.is_word(line.lower()):
        print (line)
print ("found all other words")

