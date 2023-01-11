from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.income import Income
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class IncomeBuilder(TableBuilder):

    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        #self.income_type = row[0] if 0 < len(row) else None
        #self.person_type = row[1] if 1 < len(row) else None
        owner = self.extractor.get_field_from_row(0, row)
        source = self.extractor.get_field_from_row(1, row)
        service = self.extractor.get_field_from_row(2, row)
        year_income = self.extractor.get_field_from_row(3, row)

        return Income(owner, source, service, year_income)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        owner = self.get_field_from_cells(0, cell_map)
        source = self.get_field_from_cells(1, cell_map)
        service = self.get_field_from_cells(2, cell_map)
        year_income = self.get_field_from_cells(3, cell_map)
        return Income(owner, source, service, year_income)

    def create_from_row_two_level(self, level_zero, level_one, row):
        income_type = level_zero,
        person_type = level_one
        owner = row[0] if 0 < len(row) else None
        source = row[1] if 1 < len(row) else None
        service = row[2] if 2 < len(row) else None
        year_income = row[3] if 3 < len(row) else None

        return Income(owner, source, service, year_income)

    def create_from_well_formated_line(self, line, extra_args=None):
        owner = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        source = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        service = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        year_income = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        income_type = DeclarationDataBuilder.create_from_well_formated_cell(extra_args['subtable'], 1)
        person_type = DeclarationDataBuilder.create_from_well_formated_cell(extra_args['subcategory'], 1)

        return Income(owner, source, service, year_income, income_type, person_type)