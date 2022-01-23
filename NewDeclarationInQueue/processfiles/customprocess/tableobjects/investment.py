
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Investment(TableInDocument):
    issuer = ''
    type_of_investment = ''
    number_of_shares = ''
    current_value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.issuer = row[0] if 0 < len(row) else ''
        self.type_of_investment = row[1] if 1 < len(row) else ''
        self.number_of_shares = row[2] if 2 < len(row) else ''
        self.year_of_opening = row[3] if 3 < len(row) else ''
        self.current_value = row[4] if 4 < len(row) else ''
        
    def check_validity(self):
        return len(self.issuer) > 0 or len(self.type_of_investment) > 0 or len(self.number_of_shares) > 0 or \
                len(self.current_value) > 0 
    
    def to_string(self):
        return self.issuer + ' - ' + self.type_of_investment + ' - ' + self.number_of_shares + ' - ' + \
            self.current_value
    
    def to_json(self):
        result = {
            'issuer': self.issuer,
            'type_of_investment': self.type_of_investment,
            'number_of_shares': self.number_of_shares,
            'current_value': self.current_value
        }
        
        return result