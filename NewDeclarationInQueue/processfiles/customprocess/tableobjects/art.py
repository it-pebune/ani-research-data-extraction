


from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument


class Art(TableInDocument):
    short_description = ''
    year_of_aquisition = ''
    estimated_value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.short_description = row[0] if 0 < len(row) else ''
        self.year_of_aquisition = row[1] if 1 < len(row) else ''
        self.estimated_value = row[2] if 2 < len(row) else ''
        
    def check_validity(self):
        return len(self.short_description) > 0 or len(self.year_of_aquisition) > 0 or len(self.estimated_value)
    
    def to_string(self):
        return self.short_description + ' - ' + self.year_of_aquisition + ' - ' + self.estimated_value
    
    def to_json(self):
        result = {
            'short_description': self.short_description,
            'year_of_aquisition': self.year_of_aquisition,
            'estimated_value': self.estimated_value
        }
        
        return result