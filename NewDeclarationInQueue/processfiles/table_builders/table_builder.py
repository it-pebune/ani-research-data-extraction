from abc import ABC, abstractmethod

from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData


class TableBuilder(ABC):
    """
        Builds a table from formular data
    """

    def __init__(self):
        return

    @abstractmethod
    def create_from_row(self, row):
        return None

    @abstractmethod
    def create_from_cells(self, row):
        return None

    def create_from_row_one_level(self, level_zero, row):
        return None

    def create_from_row_two_level(self, level_zero, level_one, row):
        return None

    @abstractmethod
    def create_from_well_formated_line(self, line, extra_args=None):
        return None

    def get_data_from_cell(self, cell, idx: dict) -> dict:
        data = DeclarationData()
        data.create_from_cell(cell)
        idx[str(cell['column_index'])] = data
        return idx

    def get_field_from_row(self, index: int, row: list) -> DeclarationData:
        return row[index] if index < len(row) else None

    def get_field_from_cells(self, index: int, cells: dict) -> DeclarationData:
        result = cells[str(index)] if str(index) in cells else None
        return result

    def transform_cells(self, row) -> dict:
        cell_map = {}
        for cell in row:
            cell_map = self.get_data_from_cell(cell, cell_map)

        return cell_map