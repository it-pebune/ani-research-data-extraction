from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationData, DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.art import Art


class ArtBuilder(TableBuilder):
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

    def create_from_well_formated_line(self, line, extra_args=None):
        short_description = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        year_of_aquisition = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        estimated_value = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)

        return Art(short_description, year_of_aquisition, estimated_value)