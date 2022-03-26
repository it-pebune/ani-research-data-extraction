


from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Art(TableInDocument):
    COL_SHORT_DESCRIPTION = 'short_description'
    COL_YEAR_OF_AQUISITION = 'year_of_aquisition'
    COL_ESTIMATED_VALUE = 'estimated_value'
    
    short_description: DeclarationData = None
    year_of_aquisition: DeclarationData = None
    estimated_value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.short_description = row[0] if 0 < len(row) else None
        self.year_of_aquisition = row[1] if 1 < len(row) else None
        self.estimated_value = row[2] if 2 < len(row) else None
        
    def check_validity(self):
        return self.short_description is not None or self.year_of_aquisition is not None or self.estimated_value is not None
    
    def to_string(self):
        return self.short_description.to_string() + ' - ' + self.year_of_aquisition.to_string() + ' - ' + self.estimated_value.to_string()
    
    def to_json(self):
        result = {
            self.COL_SHORT_DESCRIPTION: self.short_description.to_json() if self.short_description is not None else {},
            self.COL_YEAR_OF_AQUISITION: self.year_of_aquisition.to_json() if self.year_of_aquisition is not None else {},
            self.COL_ESTIMATED_VALUE: self.estimated_value.to_json() if self.estimated_value is not None else {}
        }
        
        return result