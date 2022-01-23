
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Debt(TableInDocument):
    lender = ''
    year_of_loan = ''
    due_year = ''
    value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.lender = row[0] if 0 < len(row) else ''
        self.year_of_loan = row[1] if 1 < len(row) else ''
        self.due_year = row[2] if 2 < len(row) else ''
        self.value = row[3] if 3 < len(row) else ''
        
    def check_validity(self):
        return len(self.lender) > 0 or len(self.year_of_loan) > 0 or len(self.due_year) > 0 or \
                len(self.value) > 0 
    
    def to_string(self):
        return self.lender + ' - ' + self.year_of_loan + ' - ' + self.due_year + ' - ' + \
            self.value
    
    def to_json(self):
        result = {
            'lender': self.lender,
            'year_of_loan': self.year_of_loan,
            'due_year': self.due_year,
            'value': self.value
        }
        
        return result