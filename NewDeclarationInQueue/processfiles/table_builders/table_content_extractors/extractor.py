from abc import abstractmethod, ABC

from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData


class Extractor(ABC):

    @abstractmethod
    def get_field_from_row(self, index: int, row: list) -> DeclarationData:
        pass

    @abstractmethod
    def get_field_from_cells(self, index: int, cells: dict) -> DeclarationData:
        pass
