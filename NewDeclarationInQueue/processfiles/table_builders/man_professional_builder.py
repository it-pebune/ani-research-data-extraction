from NewDeclarationInQueue.processfiles.table_builders.table_content_extractors.extractor import Extractor
from NewDeclarationInQueue.processfiles.table_builders.table_builder import TableBuilder
from NewDeclarationInQueue.processfiles.tableobjects.man_professional import ManProfessional


class ManProfessionalBuilder(TableBuilder):
    extractor: Extractor

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    def create_from_row(self, row):
        company = self.get_field_from_row(0, row)
        return ManProfessional(company)

    def create_from_cells(self, row):
        cell_map = self.transform_cells(row)

        company = self.get_field_from_cells(0, cell_map)

        return ManProfessional(company)