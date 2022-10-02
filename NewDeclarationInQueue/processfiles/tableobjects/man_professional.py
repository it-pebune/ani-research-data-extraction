
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class ManProfessional(TableInDocument):
    COL_COMPANY = 'name'
        
    company: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.company = self.get_field_from_row(0, row)
        
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        self.company = self.get_field_from_cells(0, cell_map)
 
        
    def check_validity(self):
        return self.company is not None 
    
    def to_string(self):
        return self.company 
    
    def to_json(self):
        result = {
            self.COL_COMPANY: self.company.to_json() if self.company is not None else {},
           
        }
        
        return result