
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Investment(TableInDocument):
    COL_ISSUER = 'issuer'
    COL_TYPE_OF_INVESTMENT = 'type_of_investment'
    COL_NUMBER_OF_SHARES = 'number_of_shares'
    COL_CURRENT_VALUE = 'current_value'
    
    issuer: DeclarationData = None
    type_of_investment: DeclarationData = None
    number_of_shares: DeclarationData = None
    current_value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.issuer = self.get_field_from_row(0, row)
        self.type_of_investment = self.get_field_from_row(1, row)
        self.number_of_shares = self.get_field_from_row(2, row)
        self.year_of_opening = self.get_field_from_row(3, row)
        self.current_value = self.get_field_from_row(4, row)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        self.issuer = self.get_field_from_cells(0, cell_map)
        self.type_of_investment = self.get_field_from_cells(1, cell_map)
        self.number_of_shares = self.get_field_from_cells(2, cell_map)
        self.year_of_opening = self.get_field_from_cells(3, cell_map)
        self.current_value = self.get_field_from_cells(4, cell_map)
        
    def check_validity(self):
        return self.issuer is not None or self.type_of_investment is not None or self.number_of_shares is not None or \
                self.current_value is not None 
    
    def to_string(self):
        return self.issuer.to_string() + ' - ' + self.type_of_investment.to_string() + ' - ' + self.number_of_shares.to_string() + ' - ' + \
            self.current_value
    
    def to_json(self):
        result = {
            self.COL_ISSUER: self.issuer.to_json() if self.issuer.to_json() is not None else {},
            self.COL_TYPE_OF_INVESTMENT: self.type_of_investment.to_json() if self.type_of_investment is not None else {},
            self.COL_NUMBER_OF_SHARES: self.number_of_shares.to_json() if self.number_of_shares is not None else {},
            self.COL_CURRENT_VALUE: self.current_value.to_json() if self.current_value is not None else {}
        }
        
        return result