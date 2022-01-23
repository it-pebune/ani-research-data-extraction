
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Income(TableInDocument):
    income_type = ''
    person_type = ''
    owner = ''
    source = ''
    service = ''
    year_income = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.income_type = row[0] if 0 < len(row) else ''
        self.person_type = row[1] if 1 < len(row) else ''
        self.owner = row[2] if 2 < len(row) else ''
        self.source = row[3] if 3 < len(row) else ''
        self.service = row[4] if 4 < len(row) else ''
        self.year_income = row[5] if 5 < len(row) else ''
        
    def create_from_row_two_level(self, level_zero, level_one, row):
        self.income_type = level_zero,
        self.person_type = level_one
        self.owner = row[0] if 0 < len(row) else ''
        self.source = row[1] if 1 < len(row) else ''
        self.service = row[2] if 2 < len(row) else ''
        self.year_income = row[3] if 3 < len(row) else ''
        
        
    def check_validity(self):
        return len(self.owner) > 0 or \
                len(self.source) > 0 or len(self.service) > 0  or len(self.year_income) > 0
    
    def to_string(self):
        return self.income_type + ' - ' + self.person_type + ' - ' + self.owner + ' - ' + \
            self.source + ' - ' + self.service + ' - ' + self.year_income
    
    def to_json(self):
        result = {
            'income_type': self.income_type,
            'person_type': self.person_type,
            'owner': self.owner,
            'source': self.source,
            'service': self.service,
            'year_income': self.year_income 
        }
        
        return result