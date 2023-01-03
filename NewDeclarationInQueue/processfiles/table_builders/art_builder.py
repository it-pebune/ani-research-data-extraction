


from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.art import Art


class ArtBuilder(OcrTableBuilder):
    COL_SHORT_DESCRIPTION = 'short_description'
    COL_YEAR_OF_AQUISITION = 'year_of_aquisition'
    COL_ESTIMATED_VALUE = 'estimated_value'
    
    # short_description: DeclarationData = None
    # year_of_aquisition: DeclarationData = None
    # estimated_value: DeclarationData = None
        
    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor
    
    def create_from_row(self, row):
        short_description = self.extractor.get_field_from_row(0, row)
        year_of_aquisition = self.extractor.get_field_from_row(1, row)
        estimated_value = self.extractor.get_field_from_row(2, row)
        
        return Art(short_description, year_of_aquisition, estimated_value)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        short_description = self.extractor.get_field_from_cells(0, cell_map)
        year_of_aquisition = self.extractor.get_field_from_cells(1, cell_map)
        estimated_value = self.extractor.get_field_from_cells(2, cell_map)
        
        return Art(short_description, year_of_aquisition, estimated_value)
        
    # def check_validity(self):
    #     return self.short_description is not None or self.year_of_aquisition is not None or self.estimated_value is not None
    
    # def to_string(self):
    #     return self.short_description.to_string() + ' - ' + self.year_of_aquisition.to_string() + ' - ' + self.estimated_value.to_string()
    
    # def to_json(self):
    #     result = {
    #         self.COL_SHORT_DESCRIPTION: self.short_description.to_json() if self.short_description is not None else {},
    #         self.COL_YEAR_OF_AQUISITION: self.year_of_aquisition.to_json() if self.year_of_aquisition is not None else {},
    #         self.COL_ESTIMATED_VALUE: self.estimated_value.to_json() if self.estimated_value is not None else {}
    #     }
        
    #     return result