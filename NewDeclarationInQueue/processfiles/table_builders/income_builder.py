
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.income import Income
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class IncomeBuilder(OcrTableBuilder):
    
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
    
    def create_from_row(self, row):
        #self.income_type = row[0] if 0 < len(row) else None
        #self.person_type = row[1] if 1 < len(row) else None
        owner = self.extractor.get_field_from_row(0, row)
        source = self.extractor.get_field_from_row(1, row)
        service = self.extractor.get_field_from_row(2, row)
        year_income = self.extractor.get_field_from_row(3, row)
        
        return Income(owner, source, service, year_income)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        owner = self.get_field_from_cells(0, cell_map)
        source = self.get_field_from_cells(1, cell_map)
        service = self.get_field_from_cells(2, cell_map)
        year_income = self.get_field_from_cells(3, cell_map)
        return Income(owner, source, service, year_income)
        
    def create_from_row_two_level(self, level_zero, level_one, row):
        income_type = level_zero,
        person_type = level_one
        owner = row[0] if 0 < len(row) else None
        source = row[1] if 1 < len(row) else None
        service = row[2] if 2 < len(row) else None
        year_income = row[3] if 3 < len(row) else None
        
        return Income(owner, source, service, year_income)
        
        
    # def check_validity(self):
    #     return self.owner is not None or \
    #             self.source is not None or self.service is not None  or self.year_income is not None
    
    # def to_string(self):
    #     #return self.income_type.to_string() + ' - ' + self.person_type.to_string() + ' - ' + 
    #     return self.owner.to_string() + ' - ' + \
    #         self.source.to_string() + ' - ' + self.service.to_string() + ' - ' + self.year_income
    
    # def to_json(self):
    #     result = {
    #         #self.COL_INCOME_TYPE: self.income_type.to_json() if self.income_type is not None else {},
    #         #self.COL_PERSON_TYPE: self.person_type.to_json() if self.person_type is not None else {},
    #         self.COL_OWNER: self.owner.to_json() if self.owner is not None else {},
    #         self.COL_SOURCE: self.source.to_json() if self.source is not None else {},
    #         self.COL_SERVICE: self.service.to_json() if self.service is not None else {},
    #         self.COL_YEAR_INCOME: self.year_income.to_json() if self.year_income is not None else {} 
    #     }
        
    #     return result