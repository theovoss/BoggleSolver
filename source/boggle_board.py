class boggle:
    def __init__ (self, num_columns = 5, num_rows = 5):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.boggle_array = [self.num_columns * self.num_rows]

    def is_adjacent(self, index_1, index_2):
        retVal = False
        if index_1 is index_2:
            retVal = True
        row_1 = index_1/self.num_columns
        row_2 = index_2/self.num_columns
        column_1 = index_1%self.num_columns
        column_2 = index_2%self.num_columns

        # check diagonal
        if (abs(row_1 - row_2) <= 1) and (abs(column_1 - column_2) <= 1):
            retVal = True

        return retVal

    def get_adjacent(self,index):
        retVal = []
        for i in range(0,self.num_columns * self.num_rows):
            if self.is_adjacent(index,i) and (i is not index):
                retVal.append(i)
        return retVal
