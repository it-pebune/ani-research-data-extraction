

class TableStopHeader:
    n_table: int
    cell: dict
    
    def __init__(self, ncount, headercell):
        self.n_table = ncount
        self.cell = headercell
    