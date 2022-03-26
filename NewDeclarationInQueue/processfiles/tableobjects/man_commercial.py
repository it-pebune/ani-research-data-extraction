
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class ManCommercial(TableInDocument):
    COL_COMPANY = 'company'
    COL_POSITION = 'position'
    COL_VALUE_OF_SHARES = 'value_of_shares'
    
    company: DeclarationData = None
    position: DeclarationData = None
    value_of_shares: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else None
        self.position = row[1] if 1 < len(row) else None
        self.value_of_shares = row[3] if 3 < len(row) else None
        
 
        
    def check_validity(self):
        return self.company is not None or self.position is not None or \
                self.value_of_shares is not None 
    
    def to_string(self):
        return self.company.to_string() + ' - ' + self.position.to_string() + ' - ' + \
            self.value_of_shares
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
            self.COL_POSITION: self.position.to_json() if self.position is not None else {},
            self.COL_VALUE_OF_SHARES: self.value_of_shares.to_json() if self.value_of_shares is not None else {}
        }
        
        return result