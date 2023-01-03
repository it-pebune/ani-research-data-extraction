
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.associate import Associate

class AssociateBuilder(OcrTableBuilder):        
    
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
            
    def create_from_row(self, row):
        company = self.extractor.get_field_from_row(0, row)
        position = self.extractor.get_field_from_row(1, row)
        no_of_shares = self.extractor.get_field_from_row(2, row)
        value_of_shares = self.extractor.get_field_from_row(3, row)
        return Associate(company, position, no_of_shares, value_of_shares)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        company = self.extractor.get_field_from_cells(0, cell_map)
        position = self.extractor.get_field_from_cells(1, cell_map)
        no_of_shares = self.extractor.get_field_from_cells(2, cell_map)
        value_of_shares = self.extractor.get_field_from_cells(3, cell_map)
        
        return Associate(company, position, no_of_shares, value_of_shares)
