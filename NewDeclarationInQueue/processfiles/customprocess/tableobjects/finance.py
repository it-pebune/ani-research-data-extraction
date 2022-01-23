
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Finance(TableInDocument):
    adm_institution = ''
    type_of_investment = ''
    currency = ''
    year_of_opening = ''
    current_value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.adm_institution = row[0] if 0 < len(row) else ''
        self.type_of_investment = row[1] if 1 < len(row) else ''
        self.currency = row[2] if 2 < len(row) else ''
        self.year_of_opening = row[3] if 3 < len(row) else ''
        self.current_value = row[4] if 4 < len(row) else ''
        
    def check_validity(self):
        return len(self.adm_institution) > 0 or len(self.type_of_investment) > 0 or len(self.currency) > 0 or \
                len(self.year_of_opening) > 0 or len(self.current_value) > 0 
    
    def to_string(self):
        return self.adm_institution + ' - ' + self.type_of_investment + ' - ' + self.currency + ' - ' + \
            self.year_of_opening + ' - ' + self.current_value
    
    def to_json(self):
        result = {
            'adm_institution': self.adm_institution,
            'type_of_investment': self.type_of_investment,
            'currency': self.currency,
            'year_of_opening': self.year_of_opening,
            'current_value': self.current_value
        }
        
        return result