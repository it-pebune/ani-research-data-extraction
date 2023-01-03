
from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData


class OcrModelBuilder():

    def get_data_from_cell(self, cell, idx: dict) -> dict:
        data = DeclarationData()
        data.create_from_cell(cell)
        idx[str(cell['column_index'])] = data
        return idx
    
    def get_field_from_row(self, index: int, row:list) -> DeclarationData:
        return row[index] if index < len(row) else None
    
    def get_field_from_cells(self, index: int, cells: dict) -> DeclarationData:
        result = cells[str(index)] if str(index) in cells else None
        return result
    
    def transform_cells(self, row) -> dict:
        cell_map = {}
        for cell in row:
            cell_map = self.get_data_from_cell(cell, cell_map)
            
        return cell_map