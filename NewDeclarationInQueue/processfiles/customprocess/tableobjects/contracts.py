
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Contracts(TableInDocument):
    owner = ''
    institution = ''
    procedure = ''
    contract_type = ''
    date_of_contract = ''
    duration = ''
    value = ''
    
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.owner = row[0] if 0 < len(row) else ''
        self.institution = row[1] if 1 < len(row) else ''
        self.procedure = row[2] if 2 < len(row) else ''
        self.contract_type = row[3] if 3 < len(row) else ''
        self.date_of_contract = row[4] if 4 < len(row) else ''
        self.duration = row[5] if 5 < len(row) else ''
        self.value = row[6] if 6 < len(row) else ''
        
 
        
    def check_validity(self):
        return len(self.owner) > 0 or len(self.institution) > 0 or \
                len(self.procedure) > 0 or len(self.contract_type) > 0 or \
                len(self.date_of_contract) > 0 or \
                len(self.duration) > 0  or len(self.value) > 0 
    
    def to_string(self):
        return self.owner + ' - ' + self.institution + ' - ' + self.procedure + ' - ' + \
            self.contract_type + ' - ' + self.date_of_contract + ' - ' + \
            self.duration + ' - ' + self.value
    
    def to_json(self):
        result = {
            'owner': self.owner,
            'institution': self.institution,
            'procedure': self.procedure,
            'contract_type': self.contract_type,
            'date_of_contract': self.date_of_contract,
            'duration': self.duration,
            'value': self.value
        }
        
        return result