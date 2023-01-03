
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.finance import Finance
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class FinanceBuilder(OcrTableBuilder):
    
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
    
    def create_from_row(self, row):
        adm_institution = self.extractor.get_field_from_row(0, row)
        type_of_investment = self.extractor.get_field_from_row(1, row)
        currency = self.extractor.get_field_from_row(2, row)
        year_of_opening = self.extractor.get_field_from_row(3, row)
        current_value = self.extractor.get_field_from_row(4, row)
        return Finance(adm_institution, type_of_investment, currency, year_of_opening, current_value)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        adm_institution = self.extractor.get_field_from_cells(0, cell_map)
        type_of_investment = self.extractor.get_field_from_cells(1, cell_map)
        currency = self.extractor.get_field_from_cells(2, cell_map)
        year_of_opening = self.extractor.get_field_from_cells(3, cell_map)
        current_value = self.extractor.get_field_from_cells(4, cell_map)
        
        return Finance(adm_institution, type_of_investment, currency, year_of_opening, current_value)
        

    # def check_validity(self):
    #     return self.adm_institution is not None or self.type_of_investment is not None or self.currency is not None or \
    #             self.year_of_opening is not None or self.current_value is not None 
    
    # def to_string(self):
    #     return self.adm_institution.to_string() + ' - ' + self.type_of_investment.to_string() + ' - ' + self.currency.to_string() + ' - ' + \
    #         self.year_of_opening.to_string() + ' - ' + self.current_value
    
    # def to_json(self):
    #     result = {
    #         self.COL_ADM_INSTITUTION: self.adm_institution.to_json() if self.adm_institution is not None else {},
    #         self.COL_TYPE_OF_INVESTMENT: self.type_of_investment.to_json() if self.type_of_investment is not None else {},
    #         self.COL_CURRENCY: self.currency.to_json() if self.currency is not None else {},
    #         self.COL_YEAR_OF_OPENING: self.year_of_opening.to_json() if self.year_of_opening is not None else {},
    #         self.COL_CURRENT_VALUE: self.current_value.to_json() if self.current_value is not None else {}
    #     }
        
    #     return result