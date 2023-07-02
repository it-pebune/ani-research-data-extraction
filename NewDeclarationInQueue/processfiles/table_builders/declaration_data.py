from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData


class DeclarationDataBuilder:

    def __init__(self):
        pass

    @staticmethod
    def create_from_row(obj) -> bool:
        if obj is None:
            return False

        value_data = obj['value_data']
        if value_data is None:
            return False

        return DeclarationData(obj['value'], value_data['page_number'], obj['confidence'], value_data['bounding_box'])

    @staticmethod
    def create_from_cell(obj) -> bool:
        if obj is None:
            return False

        return DeclarationData(obj['text'], obj['page_number'], obj['confidence'], obj['bounding_box'])

    @staticmethod
    def create_from_well_formated_cell(cell_text, page_number):
        # TODO Teodor use the output method here, after finishing the other major things
        return DeclarationData(cell_text["raw_cell"], page_number, 1, [])
