from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import \
    Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import \
    TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.mobile import Mobile


class MobileBuilder(TableBuilder):
    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        type_of_product = self.extractor.get_field_from_row(0, row)
        date_of_sale = self.extractor.get_field_from_row(1, row)
        buyer = self.extractor.get_field_from_row(2, row)
        type_of_sale = self.extractor.get_field_from_row(3, row)
        value = self.extractor.get_field_from_row(4, row)

        return Mobile(type_of_product, date_of_sale, buyer, type_of_sale, value)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        type_of_product = self.extractor.get_field_from_cells(0, cell_map)
        date_of_sale = self.extractor.get_field_from_cells(1, cell_map)
        buyer = self.extractor.get_field_from_cells(2, cell_map)
        type_of_sale = self.extractor.get_field_from_cells(3, cell_map)
        value = self.extractor.get_field_from_cells(4, cell_map)

        return Mobile(type_of_product, date_of_sale, buyer, type_of_sale, value)

    def create_from_well_formated_line(self, line, extra_args=None):
        type_of_product = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        date_of_sale = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        buyer = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        type_of_sale = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        value = DeclarationDataBuilder.create_from_well_formated_cell(line[4], 1)

        return Mobile(type_of_product, date_of_sale, buyer, type_of_sale, value)
