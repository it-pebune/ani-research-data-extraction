
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.investment import Investment
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

class InvestmentBuilder(OcrTableBuilder):
    
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
        
    def create_from_row(self, row):
        issuer = self.extractor.get_field_from_row(0, row)
        type_of_investment = self.extractor.get_field_from_row(1, row)
        number_of_shares = self.extractor.get_field_from_row(2, row)
        year_of_opening = self.extractor.get_field_from_row(3, row)
        current_value = self.extractor.get_field_from_row(4, row)
        
        return Investment(issuer, type_of_investment, number_of_shares, year_of_opening, current_value)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        issuer = self.extractor.get_field_from_cells(0, cell_map)
        type_of_investment = self.extractor.get_field_from_cells(1, cell_map)
        number_of_shares = self.extractor.get_field_from_cells(2, cell_map)
        year_of_opening = self.extractor.get_field_from_cells(3, cell_map)
        current_value = self.extractor.get_field_from_cells(4, cell_map)
        
        return Investment(issuer, type_of_investment, number_of_shares, year_of_opening, current_value)