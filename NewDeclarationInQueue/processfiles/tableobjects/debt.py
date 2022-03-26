
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Debt(TableInDocument):
    COL_LENDER = 'lender'
    COL_YEAR_OF_LOAN = 'year_of_loan'
    COL_DUE_YEAR = 'due_year'
    COL_VALUE = 'value'
    
    lender: DeclarationData = None
    year_of_loan: DeclarationData = None
    due_year: DeclarationData = None
    value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.lender = row[0] if 0 < len(row) else None
        self.year_of_loan = row[1] if 1 < len(row) else None
        self.due_year = row[2] if 2 < len(row) else None
        self.value = row[3] if 3 < len(row) else None
        
    def check_validity(self):
        return self.lender is not None or self.year_of_loan is not None or self.due_year is not None or \
                self.value is not None 
    
    def to_string(self):
        return self.lender.to_string() + ' - ' + self.year_of_loan.to_string() + ' - ' + self.due_year.to_string() + ' - ' + \
            self.value
    
    def to_json(self):
        result = {
            self.COL_LENDER: self.lender.to_json() if self.lender is not None else {},
            self.COL_YEAR_OF_LOAN: self.year_of_loan.to_json() if self.year_of_loan is not None else {},
            self.COL_DUE_YEAR: self.due_year.to_json() if self.due_year is not None else {},
            self.COL_VALUE: self.value.to_json() if self.value is not None else {}
        }
        
        return result