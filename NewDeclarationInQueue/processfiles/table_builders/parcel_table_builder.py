from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.parcel import Parcel
from NewDeclarationInQueue.processfiles.tableobjects.table_content_extractors.extractor import Extractor


class ParcelTableBuilder(TableBuilder):
    extractor: Extractor = None

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        address = self.extractor.get_field_from_row(0, row)
        category = self.extractor.get_field_from_row(1, row)
        year_of_purchase = self.extractor.get_field_from_row(2, row)
        surface = self.extractor.get_field_from_row(3, row)
        quota = self.extractor.get_field_from_row(4, row)
        type_of_aquisition = self.extractor.get_field_from_row(5, row)
        owner = self.extractor.get_field_from_row(6, row)

        return Parcel(address, category, year_of_purchase, surface, quota, type_of_aquisition, owner)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        address = self.extractor.get_field_from_cells(0, cell_map)
        category = self.extractor.get_field_from_cells(1, cell_map)
        year_of_purchase = self.extractor.get_field_from_cells(2, cell_map)
        surface = self.extractor.get_field_from_cells(3, cell_map)
        quota = self.extractor.get_field_from_cells(4, cell_map)
        type_of_aquisition = self.extractor.get_field_from_cells(5, cell_map)
        owner = self.extractor.get_field_from_cells(6, cell_map)

        return Parcel(address, category, year_of_purchase, surface, quota, type_of_aquisition, owner)

    def create_from_well_formated_line(self, line, extra_args=None):
        address = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        category = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        year_of_purchase = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        surface = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        quota = DeclarationDataBuilder.create_from_well_formated_cell(line[4], 1)
        type_of_aquisition = DeclarationDataBuilder.create_from_well_formated_cell(line[5], 1)
        owner = DeclarationDataBuilder.create_from_well_formated_cell(line[6], 1)

        return Parcel(address, category, year_of_purchase, surface, quota, type_of_aquisition, owner)
