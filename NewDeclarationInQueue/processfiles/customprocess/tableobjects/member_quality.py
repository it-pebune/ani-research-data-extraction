
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class MemberQuality(TableInDocument):
    company = ''
    position = ''
    number_of_shares = ''
    total_value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = row[0] if 0 < len(row) else ''
        self.position = row[1] if 1 < len(row) else ''
        self.number_of_shares = row[2] if 2 < len(row) else ''
        self.total_value = row[3] if 3 < len(row) else ''
        
    def check_validity(self):
        return len(self.company) > 0 or len(self.position) > 0 or len(self.number_of_shares) > 0 or \
                len(self.total_value) > 0
    
    def to_string(self):
        return self.company + ' - ' + self.position + ' - ' + self.number_of_shares + ' - ' + \
            self.total_value
    
    def to_json(self):
        result = {
            'company': self.company,
            'position': self.position,
            'number_of_shares': self.number_of_shares,
            'total_value': self.total_value
        }
        
        return result