from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.debt import Debt


class DebtBuilder(TableBuilder):

    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        lender = self.extractor.get_field_from_row(0, row)
        year_of_loan = self.extractor.get_field_from_row(1, row)
        due_year = self.extractor.get_field_from_row(2, row)
        value = self.extractor.get_field_from_row(3, row)
        return Debt(lender, year_of_loan, due_year, value)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        lender = self.extractor.get_field_from_cells(0, cell_map)
        year_of_loan = self.extractor.get_field_from_cells(1, cell_map)
        due_year = self.extractor.get_field_from_cells(2, cell_map)
        value = self.extractor.get_field_from_cells(3, cell_map)
        return Debt(lender, year_of_loan, due_year, value)

    def create_from_well_formated_line(self, line, extra_args=None):
        lender = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        year_of_loan = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        due_year = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        value = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        return Debt(lender, year_of_loan, due_year, value)