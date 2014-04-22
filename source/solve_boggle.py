from boggle_board import boggle
from load_english_dictionary import e_dict

class solve_boggle:

    def __init__(self,boggle_array,columns,rows):
        self.e_dict_path = "..\\..\\docs\\english_words.txt"
        self.e_dict = e_dict()
        self.e_dict.read_dictionary(self.e_dict_path)
        self.boggle = boggle(columns,rows)
        self.boggle.set_array(boggle_array)
