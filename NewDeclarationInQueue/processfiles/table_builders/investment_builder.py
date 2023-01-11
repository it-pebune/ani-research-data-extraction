from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import \
    Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import \
    TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.investment import \
    Investment


class InvestmentBuilder(TableBuilder):

    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        issuer = self.extractor.get_field_from_row(0, row)
        type_of_investment = self.extractor.get_field_from_row(1, row)
        number_of_shares = self.extractor.get_field_from_row(2, row)
        current_value = self.extractor.get_field_from_row(3, row)

        return Investment(issuer, type_of_investment, number_of_shares, current_value)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        issuer = self.extractor.get_field_from_cells(0, cell_map)
        type_of_investment = self.extractor.get_field_from_cells(1, cell_map)
        number_of_shares = self.extractor.get_field_from_cells(2, cell_map)
        current_value = self.extractor.get_field_from_cells(3, cell_map)

        return Investment(issuer, type_of_investment, number_of_shares, current_value)

    def create_from_well_formated_line(self, line, extra_args=None):
        issuer = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        type_of_investment = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        number_of_shares = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        current_value = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)

        return Investment(issuer, type_of_investment, number_of_shares, current_value)