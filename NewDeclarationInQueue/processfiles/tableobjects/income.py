
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Income(TableInDocument):
    #COL_INCOME_TYPE = 'income_type'
    #COL_PERSON_TYPE = 'person_type'
    COL_OWNER = 'owner'
    COL_SOURCE = 'source'
    COL_SERVICE = 'service'
    COL_YEAR_INCOME = 'year_income'
    
    income_type: DeclarationData = None
    person_type: DeclarationData = None
    owner: DeclarationData = None
    source: DeclarationData = None
    service: DeclarationData = None
    year_income: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        #self.income_type = row[0] if 0 < len(row) else None
        #self.person_type = row[1] if 1 < len(row) else None
        self.owner = self.get_field_from_row(0, row)
        self.source = self.get_field_from_row(1, row)
        self.service = self.get_field_from_row(2, row)
        self.year_income = self.get_field_from_row(3, row)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        self.owner = self.get_field_from_cells(0, cell_map)
        self.source = self.get_field_from_cells(1, cell_map)
        self.service = self.get_field_from_cells(2, cell_map)
        self.year_income = self.get_field_from_cells(3, cell_map)
        
    def create_from_row_two_level(self, level_zero, level_one, row):
        self.income_type = level_zero,
        self.person_type = level_one
        self.owner = row[0] if 0 < len(row) else None
        self.source = row[1] if 1 < len(row) else None
        self.service = row[2] if 2 < len(row) else None
        self.year_income = row[3] if 3 < len(row) else None
        
        
    def check_validity(self):
        return self.owner is not None or \
                self.source is not None or self.service is not None  or self.year_income is not None
    
    def to_string(self):
        #return self.income_type.to_string() + ' - ' + self.person_type.to_string() + ' - ' + 
        return self.owner.to_string() + ' - ' + \
            self.source.to_string() + ' - ' + self.service.to_string() + ' - ' + self.year_income
    
    def to_json(self):
        result = {
            #self.COL_INCOME_TYPE: self.income_type.to_json() if self.income_type is not None else {},
            #self.COL_PERSON_TYPE: self.person_type.to_json() if self.person_type is not None else {},
            self.COL_OWNER: self.owner.to_json() if self.owner is not None else {},
            self.COL_SOURCE: self.source.to_json() if self.source is not None else {},
            self.COL_SERVICE: self.service.to_json() if self.service is not None else {},
            self.COL_YEAR_INCOME: self.year_income.to_json() if self.year_income is not None else {} 
        }
        
        return result