
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.gift import Gift
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class GiftBuilder(OcrTableBuilder):
      
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
        
    def create_from_row(self, row):
        #self.person_type = row[0] if 0 < len(row) else None
        owner = self.extractor.get_field_from_row(0, row)
        source = self.extractor.get_field_from_row(1, row)
        service = self.extractor.get_field_from_row(2, row)
        year_income = self.extractor.get_field_from_row(3, row)
        return Gift(owner, source, service, year_income)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        owner = self.extractor.get_field_from_cells(0, cell_map)
        source = self.extractor.get_field_from_cells(1, cell_map)
        service = self.extractor.get_field_from_cells(2, cell_map)
        year_income = self.extractor.get_field_from_cells(3, cell_map)
        return Gift(owner, source, service, year_income)
        
    def create_from_row_one_level(self, level_zero, row):
        person_type = level_zero
        owner = row[0] if 0 < len(row) else None
        source = row[1] if 1 < len(row) else None
        service = row[2] if 2 < len(row) else None
        year_income = row[3] if 3 < len(row) else None
        return Gift(owner, source, service, year_income, person_type)
