from boggle_board import boggle
from load_english_dictionary import e_dict

class solve_boggle:

    def __init__(self,boggle_array,columns,rows):
        self.e_dict_path = "..\\..\\docs\\test_words.txt"
        self.e_dict = e_dict()
        self.e_dict.read_dictionary(self.e_dict_path)
        self.boggle = boggle(columns,rows)
        self.boggle.set_array(boggle_array)

    def solve(self):
        words = []
        for i,letter in enumerate(self.boggle.boggle_array):
            w = self.recurse_search_for_words(i,letter,'')
            words += w
            # print (w)
        return words

    def recurse_search_for_words(self,index,letter,word):
        retVal = []
        for indexes in self.boggle.get_adjacent(index):
            if self.e_dict.is_still_potentially_valid(word+letter):
                retVal += self.recurse_search_for_words(indexes,self.boggle.boggle_array[indexes],word+letter)
        if self.e_dict.is_word(word+letter):
            # print ("\n\nFound word!!\n\n")
            retVal.append(word+letter)
        return retVal
