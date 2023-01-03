
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import \
    Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import \
    OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.mobile import Mobile


class MobileBuilder(OcrTableBuilder):        
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
        

    def create_from_row(self, row):
        type_of_product = self.extractor.get_field_from_row(0, row)
        date_of_sale = self.extractor.get_field_from_row(1, row)
        buyer = self.extractor.get_field_from_row(2, row)
        type_of_sale = self.extractor.get_field_from_row(3, row)
        value = self.extractor.get_field_from_row(4, row)
        
        return Mobile(type_of_product,date_of_sale, buyer, type_of_sale, value)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        type_of_product = self.extractor.get_field_from_cells(0, cell_map)
        date_of_sale = self.extractor.get_field_from_cells(1, cell_map)
        buyer = self.extractor.get_field_from_cells(2, cell_map)
        type_of_sale = self.extractor.get_field_from_cells(3, cell_map)
        value = self.extractor.get_field_from_cells(4, cell_map)
        
        return Mobile(type_of_product,date_of_sale, buyer, type_of_sale, value)
        
    # def check_validity(self):
    #     return self.type_of_product is not None or self.date_of_sale is not None or self.buyer is not None or \
    #             self.type_of_sale is not None or self.value is not None 
    
    # def to_string(self):
    #     return self.type_of_product.to_string() + ' - ' + self.date_of_sale.to_string() + ' - ' + self.buyer.to_string() + ' - ' + \
    #         self.type_of_sale.to_string() + ' - ' + self.value
    
    # def to_json(self):
    #     result = {
    #         self.COL_TYPE_OF_PRODUCT: self.type_of_product.to_json() if self.type_of_product is not None else {},
    #         self.COL_DATE_OF_SALE: self.date_of_sale.to_json() if self.date_of_sale is not None else {},
    #         self.COL_BUYER: self.buyer.to_json() if self.buyer is not None else {},
    #         self.COL_TYPE_OF_SALE: self.type_of_sale.to_json() if self.type_of_sale is not None else {},
    #         self.COL_VALUE: self.value.to_json() if self.value is not None else {}
    #     }
        
    #     return result