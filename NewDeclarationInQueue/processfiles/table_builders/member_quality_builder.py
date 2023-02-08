from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.member_quality import MemberQuality
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class MemberQualityBuilder(TableBuilder):

    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        company = self.get_field_from_row(0, row)
        position = self.get_field_from_row(1, row)
        number_of_shares = self.get_field_from_row(2, row)
        total_value = self.get_field_from_row(3, row)

        return MemberQuality(company, position, number_of_shares, total_value)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        company = self.get_field_from_cells(0, cell_map)
        position = self.get_field_from_cells(1, cell_map)
        number_of_shares = self.get_field_from_cells(2, cell_map)
        total_value = self.get_field_from_cells(3, cell_map)

        return MemberQuality(company, position, number_of_shares, total_value)
    
    def create_from_well_formated_line(self, line, extra_args=None):
        return None


