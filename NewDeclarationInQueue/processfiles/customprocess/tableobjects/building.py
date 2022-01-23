
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Building(TableInDocument):
    address = ''
    category = ''
    year_of_purchase = ''
    surface = ''
    quota = ''
    type_of_aquisition = ''
    owner = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.address = row[0] if 0 < len(row) else ''
        self.category = row[1] if 1 < len(row) else ''
        self.year_of_purchase = row[2] if 2 < len(row) else ''
        self.surface = row[3] if 3 < len(row) else ''
        self.quota = row[4] if 4 < len(row) else ''
        self.type_of_aquisition = row[5] if 5 < len(row) else ''
        self.owner = row[6] if 6 < len(row) else ''
        
    def check_validity(self):
        return len(self.address) > 0 or len(self.category) > 0 or len(self.year_of_purchase) > 0 or \
                len(self.surface) > 0 or len(self.quota) > 0 or len(self.type_of_aquisition) > 0 or \
                len(self.owner) > 0
    
    def to_string(self):
        return self.address + ' - ' + self.category + ' - ' + self.year_of_purchase + ' - ' + \
            self.surface + ' - ' + self.quota + ' - ' + self.type_of_aquisition + ' - ' + \
            self.owner
    
    def to_json(self):
        result = {
            'address': self.address,
            'category': self.category,
            'year_of_purchase': self.year_of_purchase,
            'surface': self.surface,
            'quota': self.quota,
            'type_of_aquisition': self.type_of_aquisition,
            'owner': self.owner
        }
        
        return result