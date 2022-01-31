
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class ManProfessional(TableInDocument):
    company = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else ''
        
 
        
    def check_validity(self):
        return len(self.company) > 0 
    
    def to_string(self):
        return self.company 
    
    def to_json(self):
        result = {
            'company': self.company,
           
        }
        
        return result