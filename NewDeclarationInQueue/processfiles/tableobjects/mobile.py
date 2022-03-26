
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class Mobile(TableInDocument):
    COL_TYPE_OF_PRODUCT = 'type_of_product'
    COL_DATE_OF_SALE = 'date_of_sale'
    COL_BUYER = 'buyer'
    COL_TYPE_OF_SALE = 'type_of_sale'
    COL_VALUE = 'value'
    
    type_of_product: DeclarationData = None
    date_of_sale: DeclarationData = None
    buyer: DeclarationData = None
    type_of_sale: DeclarationData = None
    value: DeclarationData = None
        
    def __init__(self):
        return
    
    def create_from_row(self, row):
        self.type_of_product = row[0] if 0 < len(row) else None
        self.date_of_sale = row[1] if 1 < len(row) else None
        self.buyer = row[2] if 2 < len(row) else None
        self.type_of_sale = row[3] if 3 < len(row) else None
        self.value = row[4] if 4 < len(row) else None
        
    def check_validity(self):
        return self.type_of_product is not None or self.date_of_sale is not None or self.buyer is not None or \
                self.type_of_sale is not None or self.value is not None 
    
    def to_string(self):
        return self.type_of_product.to_string() + ' - ' + self.date_of_sale.to_string() + ' - ' + self.buyer.to_string() + ' - ' + \
            self.type_of_sale.to_string() + ' - ' + self.value
    
    def to_json(self):
        result = {
            self.COL_TYPE_OF_PRODUCT: self.type_of_product.to_json() if self.type_of_product is not None else {},
            self.COL_DATE_OF_SALE: self.date_of_sale.to_json() if self.date_of_sale is not None else {},
            self.COL_BUYER: self.buyer.to_json() if self.buyer is not None else {},
            self.COL_TYPE_OF_SALE: self.type_of_sale.to_json() if self.type_of_sale is not None else {},
            self.COL_VALUE: self.value.to_json() if self.value is not None else {}
        }
        
        return result