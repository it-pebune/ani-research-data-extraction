
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class MemberQuality(TableInDocument):
    COL_COMPANY = 'company'
    COL_POSITION = 'position'
    COL_NUMBER_OF_SHARES = 'number_of_shares'
    COL_TOTAL_VALUE = 'total_value'
    
    company: DeclarationData = None
    position: DeclarationData = None
    number_of_shares: DeclarationData = None
    total_value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else None
        self.position = row[1] if 1 < len(row) else None
        self.number_of_shares = row[2] if 2 < len(row) else None
        self.total_value = row[3] if 3 < len(row) else None
        
    def check_validity(self):
        return self.company is not None or self.position is not None or self.number_of_shares is not None or \
                self.total_value is not None
    
    def to_string(self):
        return self.company.to_string() + ' - ' + self.position.to_string() + ' - ' + self.number_of_shares.to_string() + ' - ' + \
            self.total_value
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
            self.COL_POSITION: self.position.to_json() if self.position is not None else {},
            self.COL_NUMBER_OF_SHARES: self.number_of_shares.to_json() if self.number_of_shares is not None else {},
            self.COL_TOTAL_VALUE: self.total_value.to_json() if self.total_value is not None else {}
        }
        
        return result