
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Contracts(TableInDocument):
    COL_OWNER = 'owner'
    COL_INSITUTION = 'institution'
    COL_PROCEDURE = 'procedure'
    COL_CONTRACT_TYPE = 'contract_type'
    COL_DATE_OF_CONTRACT = 'date_of_contract'
    COL_DURATION = 'duration'
    COL_VALUE = 'value'
    
    owner: DeclarationData = None
    institution: DeclarationData = None
    procedure: DeclarationData = None
    contract_type: DeclarationData = None
    date_of_contract: DeclarationData = None
    duration: DeclarationData = None
    value: DeclarationData = None
    
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.owner = row[0] if 0 < len(row) else None
        self.institution = row[1] if 1 < len(row) else None
        self.procedure = row[2] if 2 < len(row) else None
        self.contract_type = row[3] if 3 < len(row) else None
        self.date_of_contract = row[4] if 4 < len(row) else None
        self.duration = row[5] if 5 < len(row) else None
        self.value = row[6] if 6 < len(row) else None
        
 
        
    def check_validity(self):
        return self.owner is not None or self.institution is not None or \
                self.procedure is not None or self.contract_type is not None or \
                self.date_of_contract is not None or \
                self.duration is not None  or self.value is not None 
    
    def to_string(self):
        return self.owner.to_string() + ' - ' + self.institution.to_string() + ' - ' + self.procedure.to_string() + ' - ' + \
            self.contract_type.to_string() + ' - ' + self.date_of_contract.to_string() + ' - ' + \
            self.duration.to_string() + ' - ' + self.value
    
    def to_json(self):
        result = {
            self.COL_OWNER: self.owner.to_json() if self.owner is not None else {},
            self.COL_INSITUTION: self.institution.to_json() if self.institution is not None else {},
            self.COL_PROCEDURE: self.procedure.to_json() if self.procedure is not None else {},
            self.COL_CONTRACT_TYPE: self.contract_type.to_json() if self.contract_type is not None else {},
            self.COL_DATE_OF_CONTRACT: self.date_of_contract.to_json() if self.date_of_contract is not None else {},
            self.COL_DURATION: self.duration.to_json() if self.duration is not None else {},
            self.COL_VALUE: self.value.to_json() if self.value is not None else {}
        }
        
        return result