import os
from boggle_board import boggle
from load_english_dictionary import e_dict

class solve_boggle:

    def __init__(self,boggle_array,columns,rows,dict_path=os.path.join("..","..","docs","twl06.txt")):
        self.e_dict_path = dict_path
        self.e_dict = e_dict()
        self.e_dict.read_dictionary(self.e_dict_path)
        self.boggle = boggle(columns,rows)
        self.boggle.set_array(boggle_array)

    def solve(self):
        words = []
        for i,letter in enumerate(self.boggle.boggle_array):
            w = self.recurse_search_for_words(i,letter,'',[i])
            words += w
            # print (w)
        return words

    def recurse_search_for_words(self,a_index,letter,word, indexes_searched=[]):
        retVal = []
        for index in self.boggle.get_adjacent(a_index,indexes_searched):
            searched = indexes_searched + [index]
            # need to read more into parameter scope in recursion: http://stackoverflow.com/questions/14084666/python-recursive-function-variable-scope
            if self.e_dict.is_still_potentially_valid(word+letter):
                retVal += self.recurse_search_for_words(index,self.boggle.boggle_array[index],word+letter,searched)
        if self.e_dict.is_word(word+letter):
            #print ("\n\nFound word!!\n\n")
            retVal.append(word+letter)
        return retVal
