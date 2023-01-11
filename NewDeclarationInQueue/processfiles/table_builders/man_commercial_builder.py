from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import \
    Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import \
    TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.man_commercial import \
    ManCommercial


class ManCommercialBuilder(TableBuilder):
    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        company = self.get_field_from_row(0, row)
        position = self.get_field_from_row(1, row)
        value_of_shares = self.get_field_from_row(2, row)
        return ManCommercial(company, position, value_of_shares)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        company = self.get_field_from_cells(0, cell_map)
        position = self.get_field_from_cells(1, cell_map)
        value_of_shares = self.get_field_from_cells(2, cell_map)

        return ManCommercial(company, position, value_of_shares)
