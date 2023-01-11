from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.finance import Finance
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class FinanceBuilder(TableBuilder):

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

    def create_from_well_formated_line(self, line, extra_args=None):
        adm_institution = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        type_of_investment = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        currency = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        year_of_opening = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        current_value = DeclarationDataBuilder.create_from_well_formated_cell(line[4], 1)

        return Finance(adm_institution, type_of_investment, currency, year_of_opening, current_value)
