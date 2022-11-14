
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Finance(TableInDocument):
    COL_ADM_INSTITUTION = 'adm_institution'
    COL_TYPE_OF_INVESTMENT = 'type_of_investment'
    COL_CURRENCY = 'currency'
    COL_YEAR_OF_OPENING = 'year_of_opening'
    COL_CURRENT_VALUE = 'current_value'
    
    adm_institution: DeclarationData = None
    type_of_investment: DeclarationData = None
    currency: DeclarationData = None
    year_of_opening: DeclarationData = None
    current_value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.adm_institution = self.get_field_from_row(0, row)
        self.type_of_investment = self.get_field_from_row(1, row)
        self.currency = self.get_field_from_row(2, row)
        self.year_of_opening = self.get_field_from_row(3, row)
        self.current_value = self.get_field_from_row(4, row)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        self.adm_institution = self.get_field_from_cells(0, cell_map)
        self.type_of_investment = self.get_field_from_cells(1, cell_map)
        self.currency = self.get_field_from_cells(2, cell_map)
        self.year_of_opening = self.get_field_from_cells(3, cell_map)
        self.current_value = self.get_field_from_cells(4, cell_map)
        
    def check_validity(self):
        return self.adm_institution is not None or self.type_of_investment is not None or self.currency is not None or \
                self.year_of_opening is not None or self.current_value is not None 
    
    def to_string(self):
        return self.adm_institution.to_string() + ' - ' + self.type_of_investment.to_string() + ' - ' + self.currency.to_string() + ' - ' + \
            self.year_of_opening.to_string() + ' - ' + self.current_value
    
    def to_json(self):
        result = {
            self.COL_ADM_INSTITUTION: self.adm_institution.to_json() if self.adm_institution is not None else {},
            self.COL_TYPE_OF_INVESTMENT: self.type_of_investment.to_json() if self.type_of_investment is not None else {},
            self.COL_CURRENCY: self.currency.to_json() if self.currency is not None else {},
            self.COL_YEAR_OF_OPENING: self.year_of_opening.to_json() if self.year_of_opening is not None else {},
            self.COL_CURRENT_VALUE: self.current_value.to_json() if self.current_value is not None else {}
        }
        
        return result