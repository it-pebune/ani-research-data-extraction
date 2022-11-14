
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class MemberQuality(TableInDocument):
    COL_COMPANY = 'company'
    COL_POSITION = 'position'
    COL_NUMBER_OF_SHARES = 'number_of_shares'
    COL_TOTAL_VALUE = 'total_value'
    
    company: DeclarationData = None
    position: DeclarationData = None
    number_of_shares: DeclarationData = None
    total_value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = self.get_field_from_row(0, row)
        self.position = self.get_field_from_row(1, row)
        self.number_of_shares = self.get_field_from_row(2, row)
        self.total_value = self.get_field_from_row(3, row)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        self.company = self.get_field_from_cells(0, cell_map)
        self.position = self.get_field_from_cells(1, cell_map)
        self.number_of_shares = self.get_field_from_cells(2, cell_map)
        self.total_value = self.get_field_from_cells(3, cell_map)
        
    def check_validity(self):
        return self.company is not None or self.position is not None or self.number_of_shares is not None or \
                self.total_value is not None
    
    def to_string(self):
        return self.company.to_string() + ' - ' + self.position.to_string() + ' - ' + self.number_of_shares.to_string() + ' - ' + \
            self.total_value
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
            self.COL_POSITION: self.position.to_json() if self.position is not None else {},
            self.COL_NUMBER_OF_SHARES: self.number_of_shares.to_json() if self.number_of_shares is not None else {},
            self.COL_TOTAL_VALUE: self.total_value.to_json() if self.total_value is not None else {}
        }
        
        return result