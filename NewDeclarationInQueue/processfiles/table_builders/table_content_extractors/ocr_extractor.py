from abc import ABC, abstractmethod

from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import \
    DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_content_extractors.extractor import \
    Extractor


class OcrExtractor(Extractor):
    def get_field_from_row(self, index: int, row:list) -> DeclarationData:
        return row[index] if index < len(row) else None
    
    def get_field_from_cells(self, index: int, cells: dict) -> DeclarationData:
        result = cells[str(index)] if str(index) in cells else None
        return result
    
    