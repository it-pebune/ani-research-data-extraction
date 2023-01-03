
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument
from NewDeclarationInQueue.processfiles.tableobjects.transport import Transport

class TransportBuilder(OcrTableBuilder):    
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
    
    def create_from_row(self, row):
        type_of_transport = self.extractor.get_field_from_row(0, row)
        model = self.get_field_from_row(1, row)
        number_of_pieces = self.get_field_from_row(2, row)
        year_of_production = self.get_field_from_row(3, row)
        type_of_aquisition = self.get_field_from_row(4, row)
        
        return Transport(type_of_transport, model, number_of_pieces, year_of_production, type_of_aquisition)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        type_of_transport = self.get_field_from_cells(0, cell_map)
        model = self.get_field_from_cells(1, cell_map)
        number_of_pieces = self.get_field_from_cells(2, cell_map)
        year_of_production = self.get_field_from_cells(3, cell_map)
        type_of_aquisition = self.get_field_from_cells(4, cell_map)
        
        return Transport(type_of_transport, model, number_of_pieces, year_of_production, type_of_aquisition)
