
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Transport(TableInDocument):
    type_of_transport = ''
    model = ''
    number_of_pieces = ''
    year_of_production = ''
    type_of_aquisition = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.type_of_transport = row[0] if 0 < len(row) else ''
        self.model = row[1] if 1 < len(row) else ''
        self.number_of_pieces = row[2] if 2 < len(row) else ''
        self.year_of_production = row[3] if 3 < len(row) else ''
        self.type_of_aquisition = row[4] if 4 < len(row) else ''
        
    def check_validity(self):
        return len(self.type_of_transport) > 0 or len(self.model) > 0 or len(self.number_of_pieces) > 0 or \
                len(self.year_of_production) > 0 or len(self.type_of_aquisition) > 0 
    
    def to_string(self):
        return self.type_of_transport + ' - ' + self.model + ' - ' + self.number_of_pieces + ' - ' + \
            self.year_of_production + ' - ' + self.type_of_aquisition
    
    def to_json(self):
        result = {
            'type_of_transport': self.type_of_transport,
            'model': self.model,
            'number_of_pieces': self.number_of_pieces,
            'year_of_production': self.year_of_production,
            'type_of_aquisition': self.type_of_aquisition
        }
        
        return result