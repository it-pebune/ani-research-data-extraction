from NewDeclarationInQueue.processfiles.tableobjects.declaration_data import DeclarationData
from NewDeclarationInQueue.processfiles.tableobjects.table_in_document import TableInDocument


class Transport(TableInDocument):
    COL_TYPE_OF_TRANSPORT = 'type_of_transport'
    COL_MODEL = 'model'
    COL_NUMBER_OF_PIECES = 'number_of_pieces'
    COL_YEAR_OF_PRODUCTION = 'year_of_production'
    COL_TYPE_OF_AQUISITION = 'type_of_aquisition'

    type_of_transport: DeclarationData = None
    model: DeclarationData = None
    number_of_pieces: DeclarationData = None
    year_of_production: DeclarationData = None
    type_of_aquisition: DeclarationData = None

    def __init__(self, type_of_transport, model, number_of_pieces, year_of_production, type_of_acquisition):
        self.type_of_transport = type_of_transport
        self.model = model
        self.number_of_pieces = number_of_pieces
        self.year_of_production = year_of_production
        self.type_of_aquisition = type_of_acquisition

    def check_validity(self):
        return self.type_of_transport is not None or self.model is not None or self.number_of_pieces is not None or \
                self.year_of_production is not None or self.type_of_aquisition is not None

    def to_string(self):
        return self.type_of_transport.to_string() + ' - ' + self.model.to_string() + ' - ' + self.number_of_pieces.to_string() + ' - ' + \
            self.year_of_production.to_string() + ' - ' + self.type_of_aquisition

    def to_json(self):
        result = {
            self.COL_TYPE_OF_TRANSPORT:
                self.type_of_transport.to_json() if self.type_of_transport is not None else {},
            self.COL_MODEL:
                self.model.to_json() if self.model is not None else {},
            self.COL_NUMBER_OF_PIECES:
                self.number_of_pieces.to_json() if self.number_of_pieces is not None else {},
            self.COL_YEAR_OF_PRODUCTION:
                self.year_of_production.to_json() if self.year_of_production is not None else {},
            self.COL_TYPE_OF_AQUISITION:
                self.type_of_aquisition.to_json() if self.type_of_aquisition is not None else {}
        }

        return result