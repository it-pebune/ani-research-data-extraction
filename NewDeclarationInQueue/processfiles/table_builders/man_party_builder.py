from NewDeclarationInQueue.processfiles.table_builders.declaration_data import DeclarationDataBuilder
from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.associate import Associate
from NewDeclarationInQueue.processfiles.tableobjects.man_party import ManParty


class ManagementPartyBuilder(TableBuilder):

    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        party = self.extractor.get_field_from_row(0, row)
        return ManParty(party)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        party = self.extractor.get_field_from_cells(0, cell_map)
        return ManParty(party)

    def create_from_well_formated_line(self, line, extra_args=None):
        party = DeclarationDataBuilder.create_from_well_formated_cell(line[0], 1)

        return ManParty(party)
