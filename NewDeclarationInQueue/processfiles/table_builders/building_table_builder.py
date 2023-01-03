
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_in_document import OcrTableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.building import Building
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument

# TODO: these are not actually tables, are just rows
class BuildingTableBuilder(OcrTableBuilder):

    extractor: Extractor
        
    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        address = self.get_field_from_row(0, row)
        category = self.get_field_from_row(1, row)
        year_of_purchase = self.get_field_from_row(2, row)
        surface = self.get_field_from_row(3, row)
        quota = self.get_field_from_row(4, row)
        type_of_aquisition = self.get_field_from_row(5, row)
        owner = self.get_field_from_row(6, row)
        
        return Building(address, category, year_of_purchase, surface, quota, type_of_aquisition, owner)
        
    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)
        
        address = self.get_field_from_cells(0, cell_map)
        category = self.get_field_from_cells(1, cell_map)
        year_of_purchase = self.get_field_from_cells(2, cell_map)
        surface = self.get_field_from_cells(3, cell_map)
        quota = self.get_field_from_cells(4, cell_map)
        type_of_aquisition = self.get_field_from_cells(5, cell_map)
        owner = self.get_field_from_cells(6, cell_map)
        
        return Building(address, category, year_of_purchase, surface, quota, type_of_aquisition, owner)
        
    # def check_validity(self):
    #     return self.address is not None or self.category is not None or self.year_of_purchase is not None or \
    #             self.surface is not None or self.quota is not None or self.type_of_aquisition is not None or \
    #             self.owner is not None
    
    # def to_string(self):
    #     return self.address.to_string() + ' - ' + self.category.to_string() + ' - ' + self.year_of_purchase.to_string() + ' - ' + \
    #         self.surface.to_string() + ' - ' + self.quota.to_string() + ' - ' + self.type_of_aquisition.to_string() + ' - ' + \
    #         self.owner
    
    # def to_json(self):
    #     result = {
    #         self.COL_ADDRESS: self.address.to_json() if self.address is not None else {},
    #         self.COL_CATEGORY: self.category.to_json() if self.category is not None else {},
    #         self.COL_YEAR_OF_PURCHASE: self.year_of_purchase.to_json() if self.year_of_purchase is not None else {},
    #         self.COL_SURFACE: self.surface.to_json() if self.surface is not None else {},
    #         self.COL_QUOTA: self.quota.to_json() if self.quota is not None else {},
    #         self.COL_TYPE_OF_AQUISITION: self.type_of_aquisition.to_json() if self.type_of_aquisition is not None else {},
    #         self.COL_OWNER: self.owner.to_json() if self.owner is not None else {}
    #     }
        
    #     return result