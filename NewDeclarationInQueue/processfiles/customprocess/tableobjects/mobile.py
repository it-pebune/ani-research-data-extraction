
from NewDeclarationInQueue.processfiles.customprocess.tableobjects.table_in_document import TableInDocument

class Mobile(TableInDocument):
    type_of_product = ''
    date_of_sale = ''
    buyer = ''
    type_of_sale = ''
    value = ''
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.type_of_product = row[0] if 0 < len(row) else ''
        self.date_of_sale = row[1] if 1 < len(row) else ''
        self.buyer = row[2] if 2 < len(row) else ''
        self.type_of_sale = row[3] if 3 < len(row) else ''
        self.value = row[4] if 4 < len(row) else ''
        
    def check_validity(self):
        return len(self.type_of_product) > 0 or len(self.date_of_sale) > 0 or len(self.buyer) > 0 or \
                len(self.type_of_sale) > 0 or len(self.value) > 0 
    
    def to_string(self):
        return self.type_of_product + ' - ' + self.date_of_sale + ' - ' + self.buyer + ' - ' + \
            self.type_of_sale + ' - ' + self.value
    
    def to_json(self):
        result = {
            'type_of_product': self.type_of_product,
            'date_of_sale': self.date_of_sale,
            'buyer': self.buyer,
            'type_of_sale': self.type_of_sale,
            'value': self.value
        }
        
        return result