
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class ManProfessional(TableInDocument):
    COL_COMPANY = 'name'
    
    company: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else None
        
 
        
    def check_validity(self):
        return self.company is not None 
    
    def to_string(self):
        return self.company 
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
           
        }
        
        return result