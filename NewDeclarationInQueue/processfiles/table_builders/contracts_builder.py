from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.tableobjects.contracts import Contracts
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class ContractsBuilder(TableInDocument):
    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        owner = self.extractor.get_field_from_row(0, row)
        institution = self.extractor.get_field_from_row(1, row)
        procedure = self.extractor.get_field_from_row(2, row)
        contract_type = self.extractor.get_field_from_row(3, row)
        date_of_contract = self.extractor.get_field_from_row(4, row)
        duration = self.extractor.get_field_from_row(5, row)
        value = self.extractor.get_field_from_row(6, row)

        return Contracts(owner, institution, procedure, contract_type, date_of_contract, duration, value)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        owner = self.extractor.get_field_from_cells(0, cell_map)
        institution = self.extractor.get_field_from_cells(1, cell_map)
        procedure = self.extractor.get_field_from_cells(2, cell_map)
        contract_type = self.extractor.get_field_from_cells(3, cell_map)
        date_of_contract = self.extractor.get_field_from_cells(4, cell_map)
        duration = self.extractor.get_field_from_cells(5, cell_map)
        value = self.extractor.get_field_from_cells(6, cell_map)

        return Contracts(owner, institution, procedure, contract_type, date_of_contract, duration, value)

    def create_from_well_formated_line(self, line, extra_args=None):
        owner = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)
        institution = DeclarationDataBuilder.create_from_well_formated_cell(line[1], 1)
        procedure = DeclarationDataBuilder.create_from_well_formated_cell(line[2], 1)
        contract_type = DeclarationDataBuilder.create_from_well_formated_cell(line[3], 1)
        date_of_contract = DeclarationDataBuilder.create_from_well_formated_cell(line[4], 1)
        duration = DeclarationDataBuilder.create_from_well_formated_cell(line[5], 1)
        value = DeclarationDataBuilder.create_from_well_formated_cell(line[6], 1)
        person_type = extra_args['subcategory']

        return Contracts(owner, institution, procedure, contract_type, date_of_contract, duration, value, person_type)
