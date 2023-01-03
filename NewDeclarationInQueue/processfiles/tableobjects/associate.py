
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Associate(TableInDocument):
    COL_COMPANY = 'company'
    COL_POSITION = 'position'
    COL_NO_OF_SHARES = 'no_of_shares'
    COL_VALUE_OF_SHARES = 'value_of_shares'
    
    company: DeclarationData = None
    position: DeclarationData = None
    no_of_shares: DeclarationData = None
    value_of_shares: DeclarationData = None
        
    def __init__(self, company, position, no_of_shares, value_of_shares):
        self.company = company
        self.position = position
        self.no_of_shares = no_of_shares
        self.value_of_shares = value_of_shares
        
    def check_validity(self):
        return self.company is not None or self.position is not None or \
                self.no_of_shares is not None or self.value_of_shares is not None
    
    def to_string(self):
        return self.company.to_string() + ' - ' + self.position.to_string() + ' - ' + self.no_of_shares.to_string() + ' - ' + \
            self.value_of_shares.to_string()
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
            self.COL_POSITION: self.position.to_json() if self.position is not None else {},
            self.COL_NO_OF_SHARES: self.no_of_shares.to_json() if self.no_of_shares is not None else {},
            self.COL_VALUE_OF_SHARES: self.value_of_shares.to_json() if self.value_of_shares is not None else {}
        }
        
        return result