
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class ManCommercial(TableInDocument):
    company = ''
    position = ''
    value_of_shares = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else ''
        self.position = row[1] if 1 < len(row) else ''
        self.value_of_shares = row[3] if 3 < len(row) else ''
        
 
        
    def check_validity(self):
        return len(self.company) > 0 or len(self.position) > 0 or \
                len(self.value_of_shares) > 0 
    
    def to_string(self):
        return self.company + ' - ' + self.position + ' - ' + \
            self.value_of_shares
    
    def to_json(self):
        result = {
            'company': self.company,
            'position': self.position,
            'value_of_shares': self.value_of_shares
        }
        
        return result