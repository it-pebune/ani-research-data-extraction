
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
        
    def __init__(self, type_of_product, date_of_sale, buyer, type_of_sale, value):
        self.type_of_product = type_of_product
        self.date_of_sale = date_of_sale
        self.buyer = buyer
        self.type_of_sale = type_of_sale
        self.value = value
    
    # def create_from_row(self, row):
    #     self.type_of_product = self.get_field_from_row(0, row)
    #     self.date_of_sale = self.get_field_from_row(1, row)
    #     self.buyer = self.get_field_from_row(2, row)
    #     self.type_of_sale = self.get_field_from_row(3, row)
    #     self.value = self.get_field_from_row(4, row)
    #     return self
        
    # def create_from_cells(self, row):
    #     cell_map = self.transform_cells(row)

    #     self.type_of_product = self.get_field_from_cells(0, cell_map)
    #     self.date_of_sale = self.get_field_from_cells(1, cell_map)
    #     self.buyer = self.get_field_from_cells(2, cell_map)
    #     self.type_of_sale = self.get_field_from_cells(3, cell_map)
    #     self.value = self.get_field_from_cells(4, cell_map)
    #     return self
        
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